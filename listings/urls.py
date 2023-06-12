from django.urls import path
from .views import listings_list, listings_detail, get_address_predictions


app_name = 'listings'

urlpatterns = [
    path('get_address_predictions/', get_address_predictions, name='get_address_predictions'),
    path('<int:id>/', listings_detail, name='detail'),
    path('', listings_list, name='list'),
]