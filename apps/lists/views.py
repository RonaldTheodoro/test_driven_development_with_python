from django.shortcuts import redirect
from django.shortcuts import render

from apps.lists import models


def index(request):
    return render(request, 'index.html')


def view_list(request, list_id):
    list_ = models.List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    list_ = models.List.objects.create()
    models.Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    list_ = models.List.objects.get(id=list_id)
    models.Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')