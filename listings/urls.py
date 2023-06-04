from django.urls import path
from .views import listings_list, listings_detail


app_name = 'listings'

urlpatterns = [
    path('<int:id>/', listings_detail, name='detail'),
    path('', listings_list, name='list'),
]