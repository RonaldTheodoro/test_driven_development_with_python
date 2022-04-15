import re
from django.shortcuts import redirect
from django.shortcuts import render

from apps.lists import models


def index(request):
    return render(request, 'index.html')


def view_list(request):
    items = models.Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = models.List.objects.create()
    models.Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
