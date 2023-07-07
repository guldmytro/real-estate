from django.urls import path
from .views import wishlist_archive, wishlist_count

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_archive, name='archive'),
    path('count/', wishlist_count, name='count'),
]