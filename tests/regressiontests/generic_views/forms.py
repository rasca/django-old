from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import BaseModelFormSet, BaseInlineFormSet

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


class ArticleFormSet(BaseFormSet):
    form = ArticleForm


class AuthorFormSet(BaseFormSet):
    form = AuthorForm


class ArticleModelFormSet(BaseModelFormSet):
    model = Article


class AuthorModelFormSet(BaseModelFormSet):
    model = Author


class ArticleInlineFormSet(BaseInlineFormSet):
    model = Article
