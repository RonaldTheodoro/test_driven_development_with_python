from django.shortcuts import render


def index(request):
    context = {'new_item_text': request.POST.get('item_text', '')}
    return render(request, 'index.html', context)

