from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from apps.lists import views


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.index(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
