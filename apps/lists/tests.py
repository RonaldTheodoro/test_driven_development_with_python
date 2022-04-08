from django.test import TestCase
from django.urls import resolve

from apps.lists.views import index


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)
