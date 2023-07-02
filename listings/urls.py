from django.urls import path
from .views import listings_list, listings_detail, \
    get_address_predictions, get_listings_count, \
    get_listings_coordinates


app_name = 'listings'

urlpatterns = [
    path('get_listings_count/', get_listings_count, name='get_listings_count'),
    path('get_address_predictions/', get_address_predictions, name='get_address_predictions'),
    path('get_listings_coordinates/', get_listings_coordinates, name='get_listings_coordinates'),
    path('<int:id>/', listings_detail, name='detail'),
    path('', listings_list, name='list'),
]