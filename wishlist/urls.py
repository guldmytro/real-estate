from django.urls import path
from .views import wishlist_archive

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_archive, name='archive'),
]