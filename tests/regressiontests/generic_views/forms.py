from django import forms
from django.forms.formsets import formset_factory

from django.views.generic import (EnhancedFormSet, EnhancedModelFormSet,
                                     EnhancedInlineFormSet, )
from regressiontests.generic_views.models import Author, Article


class AuthorForm(forms.ModelForm):
    name = forms.CharField()
    slug = forms.SlugField()

    class Meta:
        model = Author


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('author', )


class ArticleEnhancedFormSet(EnhancedFormSet):
    form_class = ArticleForm


class AuthorEnhancedFormSet(EnhancedFormSet):
    form_class = AuthorForm


class ArticleEnhancedModelFormSet(EnhancedModelFormSet):
    model = Article


class AuthorEnhancedModelFormSet(EnhancedModelFormSet):
    model = Author


class ArticleEnhancedInlineFormSet(EnhancedInlineFormSet):
    model = Article
