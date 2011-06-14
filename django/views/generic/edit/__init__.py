from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit.base import (BaseFormView, BaseCreateView,
                                BaseUpdateView, BaseDeleteView, BaseFormSetView,
                                BaseModelFormSetView, BaseInlineFormSetView, )
from django.views.generic.edit.forms import (FormMixin, ModelFormMixin,
                                    ProcessFormView, DeletionMixin, )
from django.views.generic.edit.formset import (EnhancedFormSet,
                                   EnhancedModelFormSet, EnhancedInlineFormSet,
                                   FormSetMixin, ModelFormSetMixin,
                                   InlineFormSetMixin, ProcessFormSetView,
                                   ProcessInlineFormSetView, )


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

