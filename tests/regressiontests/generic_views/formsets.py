from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import FormSetMixin, ModelFormSetMixin
from regressiontests.generic_views.models import Author, Article


class FormSetViewTests(TestCase):
    urls = 'regressiontests.generic_views.urls'

    def setUp(self):
        self.data = {
            'form-TOTAL_FORMS': u'3',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-title': u'',
            'form-0-pubdate': u'',
            'form-1-title': u'',
            'form-1-pubdate': u'',
            'form-2-title': u'',
            'form-2-pubdate': u'',

            'form-2-TOTAL_FORMS': u'3',
            'form-2-INITIAL_FORMS': u'0',
            'form-2-MAX_NUM_FORMS': u'',
            'form-2-0-name': u'',
            'form-2-0-slug': u'',
            'form-2-1-name': u'',
            'form-2-1-slug': u'',
            'form-2-2-name': u'',
            'form-2-2-slug': u'',
        }

    def test_get(self):
        response = self.client.get('/edit/formsets/')
        self.assertEqual(response.status_code, 200)

    def test_empty_post(self):
        response = self.client.post('/edit/formsets/', self.data)
        self.assertEqual(response.status_code, 302)

    def test_valid(self):
        self.data.update({
            'form-0-title': u'first title',
            'form-0-pubdate': u'2011-01-13',
            'form-1-title': u'second title',
            'form-1-pubdate': u'2011-01-13',
            'form-2-0-name': u'this is my name',
            'form-2-0-slug': u'this-is-my-name',
        })
        response = self.client.post('/edit/formsets/', self.data)
        self.assertEqual(response.status_code, 302)

    def test_invalid(self):
        self.data.update({
            'form-0-title': u'first title',
            'form-0-pubdate': u'',
        })
        response = self.client.post('/edit/formsets/', self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ERROR')


class ModelFormSetViewTests(TestCase):
    urls = 'regressiontests.generic_views.urls'

    def setUp(self):
        self.data = {
            'form-TOTAL_FORMS': u'3',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-title': u'',
            'form-0-pubdate': u'',
            'form-1-title': u'',
            'form-1-pubdate': u'',
            'form-2-title': u'',
            'form-2-pubdate': u'',

            'form-2-TOTAL_FORMS': u'3',
            'form-2-INITIAL_FORMS': u'0',
            'form-2-MAX_NUM_FORMS': u'',
            'form-2-0-name': u'',
            'form-2-1-name': u'',
            'form-2-2-name': u'',
        }

    def test_get(self):
        response = self.client.get('/edit/modelformsets/')
        self.assertEqual(response.status_code, 200)

    def test_empty_post(self):
        response = self.client.post('/edit/modelformsets/', self.data)
        self.assertEqual(response.status_code, 302)

    def test_valid(self):
        self.data.update({
            'form-0-title': u'first title',
            'form-0-pubdate': u'2011-01-13',
            'form-1-title': u'second title',
            'form-1-pubdate': u'2011-01-13',
            'form-2-0-name': u'this is my name',
            'form-2-0-slug': u'this-is-my-name',
        })
        response = self.client.post('/edit/modelformsets/', self.data)
        self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_invalid(self):
        self.data.update({
            'form-0-title': u'first title',
            'form-0-pubdate': u'',
        })
        response = self.client.post('/edit/modelformsets/', self.data)
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ERROR')


class InlineFormSetViewTests(TestCase):
    urls = 'regressiontests.generic_views.urls'

    def setUp(self):
        self.formsetmgmt = {
            'article_set-TOTAL_FORMS': u'3',
            'article_set-INITIAL_FORMS': u'0',
            'article_set-MAX_NUM_FORMS': u'',
        }
        self.formsetdata = {
            'article_set-0-title': u'title1',
            'article_set-0-pubdate': u'2011-01-26',
            'article_set-1-title': u'title2',
            'article_set-1-pubdate': u'2011-01-26',
            'article_set-2-title': u'title3',
            'article_set-2-pubdate': u'2011-01-26',
        }
        self.formdata = {
            'name': u'this is my name',
            'slug': u'this-is-my-name',
        }

    def test_get(self):
        response = self.client.get('/edit/inlineformsets/')
        self.assertEqual(response.status_code, 200)

    def test_empty_post(self):
        data = {
            'article_set-TOTAL_FORMS': u'3',
            'article_set-INITIAL_FORMS': u'0',
            'article_set-MAX_NUM_FORMS': u'',
            'article_set-0-title': u'',
            'article_set-0-pubdate': u'',
            'article_set-1-title': u'',
            'article_set-1-pubdate': u'',
            'article_set-2-title': u'',
            'article_set-2-pubdate': u'',
            'name': u'',
        }
        response = self.client.post('/edit/inlineformsets/', data)
        self.assertEqual(response.status_code, 200)

    def test_valid(self):
        data = self.formdata
        data.update(self.formsetdata)
        data.update(self.formsetmgmt)
        response = self.client.post('/edit/inlineformsets/', data)
        self.assertEqual(Article.objects.count(), 3)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_no_form(self):
        data = self.formsetdata
        data.update(self.formsetmgmt)
        response = self.client.post('/edit/inlineformsets/', data)
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ERROR')

    def test_no_formset(self):
        data = self.formdata
        data.update(self.formsetmgmt)
        response = self.client.post('/edit/inlineformsets/', data)
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
