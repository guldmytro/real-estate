from django.urls import path
from .views import listings_list, listings_detail, \
    get_address_predictions, get_listings_count, \
    get_listings_coordinates, listing_detail_map
from django.views.decorators.cache import cache_page
from django.conf import settings

app_name = 'listings'

urlpatterns = [
    path('by-type/<slug:realty_type>/', listings_list, name='by_type'),
    path('by-type/<slug:realty_type>/count/', get_listings_count, name='by_type_count'),
    path('by-deal/<slug:realty_deal>/', listings_list, name='by_deal'),
    path('by-deal/<slug:realty_deal>/count/', get_listings_count, name='by_deal_count'),
    path('get_listings_count/', get_listings_count, name='get_listings_count'),
    path('get_address_predictions/', get_address_predictions, name='get_address_predictions'),
    path('get_listings_coordinates/', get_listings_coordinates, name='get_listings_coordinates'),
    path('<int:listing_id>/map/', cache_page(settings.CACHE_TIME)(listing_detail_map), name='detail_map'),
    path('<int:id>/', cache_page(settings.CACHE_TIME)(listings_detail), name='detail'),
    path('', listings_list, name='list'),
]