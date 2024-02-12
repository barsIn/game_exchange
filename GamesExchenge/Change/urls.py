from django.urls import path

from .views import index, second, about

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about')
]