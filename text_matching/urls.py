from django.urls import path
from .views import search, index


app_name = 'text_matching'

urlpatterns = [
    path('search', search, name='search'),
    path('', index, name='index'),
]
