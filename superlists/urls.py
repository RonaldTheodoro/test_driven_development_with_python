from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

from apps.lists import views as lists_views
from apps.lists import urls as list_urls


urlpatterns = [
    url(r'^$', lists_views.index, name='index'),
    url(r'^lists/', include(list_urls)),
]
