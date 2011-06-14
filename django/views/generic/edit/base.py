from django.views.generic.detail import BaseDetailView
from django.views.generic.base import View
from django.views.generic.edit.forms import (FormMixin, ModelFormMixin,
                                             ProcessFormView, DeletionMixin, )
from django.views.generic.edit.formset import (FormSetMixin, ModelFormSetMixin,
                                        InlineFormSetMixin, ProcessFormSetView,
                                        ProcessInlineFormSetView, )


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
