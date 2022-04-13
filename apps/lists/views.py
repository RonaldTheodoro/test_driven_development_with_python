from django.shortcuts import redirect
from django.shortcuts import render

from apps.lists import models


def index(request):
    if request.method == 'POST':
        models.Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = models.Item.objects.all()
    return render(request, 'index.html', {'items': items})

