from hashlib import new
from urllib import response
from django.test import TestCase

from apps.lists import models


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = models.List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_items_for_that_list(self):
        correct_list = models.List.objects.create()
        models.Item.objects.create(text='itemey 1', list=correct_list)
        models.Item.objects.create(text='itemey 2', list=correct_list)

        other_list = models.List.objects.create()
        models.Item.objects.create(text='other list item 1', list=other_list)
        models.Item.objects.create(text='other list itefm 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list itefm 2')

    def test_passes_correct_list_to_template(self):
        other_list = models.List.objects.create()
        correct_list = models.List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(models.Item.objects.count(), 1)
        new_item = models.Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        data = {'item_text': 'A new list item'}
        response = self.client.post('/lists/new', data=data)
        new_list = models.List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = models.List()
        list_.save()

        first_item = models.Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = models.Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = models.List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = models.Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = models.List.objects.create()
        correct_list = models.List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(models.Item.objects.count(), 1)
        new_item = models.Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        other_list = models.List.objects.create()
        correct_list = models.List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
