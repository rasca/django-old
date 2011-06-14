from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView,
                                     WeekArchiveView, DayArchiveView, TodayArchiveView,
                                     DateDetailView)
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.views.generic.formsets import (FormSetView, ModelFormSetView,
                               InlineFormSetView, EnhancedFormSet,
                               EnhancedModelFormSet, EnhancedInlineFormSet, )


class GenericViewError(Exception):
    """A problem in a generic view."""
    pass
