from django.urls import path
from .views import listings_list


app_name = 'listings'

urlpatterns = [
    path('', listings_list, name='list'),
]