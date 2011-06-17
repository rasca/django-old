from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory, BaseFormSet, all_valid
from django.forms.models import (modelform_factory, modelformset_factory, inlineformset_factory,
                                 BaseModelFormSet, BaseInlineFormSet, ModelForm)

from django.views.generic.detail import (SingleObjectTemplateResponseMixin,
                                         BaseDetailView, SingleObjectMixin, )
from django.views.generic.base import TemplateResponseMixin, View


class FormMixin(object):
    """
    A mixin that provides a way to show and handle a form in a request.
    """

    initial = {}
    form_class = None
    success_url = None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        return kwargs

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ModelFormMixin(FormMixin, SingleObjectMixin):
    """
    A mixin that provides a way to show and handle a modelform in a request.
    """

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        if self.form_class:
            return self.form_class
        else:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model
            return modelform_factory(model)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        return kwargs

    def get_success_url(self):
        if self.success_url:
            url = self.success_url % self.object.__dict__
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def form_valid(self, form):
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = kwargs
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        return context


class ProcessFormView(View):
    """
    A mixin that processes a form on POST.
    """
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class DeletionMixin(object):
    """
    A mixin providing the ability to delete objects
    """
    success_url = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    # Add support for browsers which only accept GET and POST for now.
    def post(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class FormSetMixin(object):
    """
    A mixin that provides a way to show and handle formsets
    """

    formsets = []  # must be a list of BaseFormSet subclasses
    success_url = None

    def construct_formsets(self):
        """
        Constructs the formsets
        """
        self.formsets_instances = []

        prefixes = {}
        for formset in self.formsets:
            # calculate prefix
            prefix = formset.get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])

            self.formsets_instances.append(
                formset(prefix=prefix, **self.get_formsets_kwargs(formset))
            )

    def get_formsets_kwargs(self, formset):
        """"
        Returns the keyword arguments for instanciating the formsets
        """

        # default kwargs
        kwargs = {}

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = {
            'formsets': [formset for formset in self.formsets_instances],
        }

        context_data.update(kwargs)
        return context_data

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url")
        return url

    def formsets_valid(self):
        return HttpResponseRedirect(self.get_success_url())

    def formsets_invalid(self):
        return self.render_to_response(self.get_context_data())


class ModelFormSetMixin(FormSetMixin):
    """
    A mixin that provides a way to show and handle model formsets
    """

    def formsets_valid(self):
        for formset in self.formsets_instances:
            formset.save()
        return super(ModelFormSetMixin, self).formsets_valid()


class InlineFormSetMixin(ModelFormSetMixin, ModelFormMixin):
    """ 
    A mixin that provides a way to show and handle a model with it's inline
    formsets
    """
    def get_formsets_kwargs(self, formset):
        """"
        Returns the keyword arguments for instanciating the inline formsets
        """
        kwargs = super(InlineFormSetMixin, self).get_formsets_kwargs(formset)
        kwargs.update({
            'instance': self.object,
            'parent_model': self.object.__class__,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Adds the context data from both parents
        """
        context_data = ModelFormSetMixin.get_context_data(self)
        context_data.update(ModelFormMixin.get_context_data(self, **kwargs))
        return context_data

    def form_valid(self, form):
        self.object.save()
        form.save_m2m()
        for formset in self.formsets_instances:
            formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    # UGLY UGLY hack follows: we can't call the get_default_prefix of the
    # formset cause it's a @classmethod and now we are generating the fk in the
    # __init__ instead than in the factory
    def get_default_prefix(self, formset):
        from django.forms.models import _get_foreign_key
        fk = _get_foreign_key(self.object.__class__, formset.model,
                                   fk_name=formset.fk_name)
        from django.db.models.fields.related import RelatedObject
        return RelatedObject(fk.rel.to, formset.model, fk).get_accessor_name().replace('+','')

    # UGLY UGLY hack continues: we use the above get_default_prefix
    def construct_formsets(self):
        """
        Constructs the formsets
        """
        self.formsets_instances = []

        prefixes = {}
        for formset in self.formsets:
            # calculate prefix
            prefix = self.get_default_prefix(formset)
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])

            self.formsets_instances.append(
                formset(prefix=prefix, **self.get_formsets_kwargs(formset))
            )


class ProcessFormSetView(View):
    """
    A mixin that processes formsets on POST
    """
    def get(self, request, *args, **kwargs):
        self.construct_formsets()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.construct_formsets()
        if all_valid(self.formsets_instances):
            return self.formsets_valid()
        else:
            return self.formsets_invalid()

    def put(self, request, *args, **kwargs):
        return self.post(*args, **kwargs)


class ProcessInlineFormSetView(View):
    """
    A mixin that processes a model instance and it's inline formsets on POST
    """

    def get(self, request, *args, **kwargs):
        # Create or Update
        try:
            self.object = self.get_object()
        except AttributeError:
            self.object = self.model()

        # ProcessFormView
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # ProcessFormSetView
        self.construct_formsets()

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Create or Update
        try:
            self.object = self.get_object()
        except AttributeError:
            self.object = self.model()

        # ProcessFormView
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.object = form.save(commit=False)

            # ProcessFormSetViewV
            self.construct_formsets()

            if all_valid(self.formsets_instances):
                return self.form_valid(form)
        else:
            # ProcessFormSetViewV
            self.construct_formsets()
        return self.form_invalid(form)


    def put(self, request, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseFormView(FormMixin, ProcessFormView):
    """
    A base view for displaying a form
    """


class BaseCreateView(ModelFormMixin, ProcessFormView):
    """
    Base view for creating an new object instance.

    Using this base class requires subclassing to provide a response mixin.
    """
    def get(self, request, *args, **kwargs):
        self.object = None
        return super(BaseCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(BaseCreateView, self).post(request, *args, **kwargs)


class BaseUpdateView(ModelFormMixin, ProcessFormView):
    """
    Base view for updating an existing object.

    Using this base class requires subclassing to provide a response mixin.
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseUpdateView, self).post(request, *args, **kwargs)


class BaseDeleteView(DeletionMixin, BaseDetailView):
    """
    Base view for deleting an object.

    Using this base class requires subclassing to provide a response mixin.
    """


class BaseFormSetView(FormSetMixin, ProcessFormSetView):
    """
    A base view for displaying formsets
    """


class BaseModelFormSetView(ModelFormSetMixin, ProcessFormSetView):
    """
    A base view for displaying model formsets
    """


class BaseInlineFormSetView(InlineFormSetMixin, ProcessInlineFormSetView):
    """
    A base view for displaying a model instance with it's inline formsets
    """


class FormView(TemplateResponseMixin, BaseFormView):
    """
    A view for displaying a form, and rendering a template response.
    """


class CreateView(SingleObjectTemplateResponseMixin, BaseCreateView):
    """
    View for creating an new object instance,
    with a response rendered by template.
    """
    template_name_suffix = '_form'


class UpdateView(SingleObjectTemplateResponseMixin, BaseUpdateView):
    """
    View for updating an object,
    with a response rendered by template..
    """
    template_name_suffix = '_form'


class DeleteView(SingleObjectTemplateResponseMixin, BaseDeleteView):
    """
    View for deleting an object retrieved with `self.get_object()`,
    with a response rendered by template.
    """
    template_name_suffix = '_confirm_delete'


class FormSetView(TemplateResponseMixin, BaseFormSetView):
    """
    A view for displaying formsets, and rendering a template response
    """


class ModelFormSetView(TemplateResponseMixin, BaseModelFormSetView):
    """
    A view for displaying model formsets, and rendering a template response
    """


class InlineFormSetView(SingleObjectTemplateResponseMixin,
                         BaseInlineFormSetView):
    """
    A view for displaying a model instance with it's inline formsets, and
    rendering a template response
    """
    template_name_suffix = '_form'
