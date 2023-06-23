from django.urls import path
from .views import discounts_list, discounts_detail

app_name = 'discounts'

urlpatterns = [
    path('<slug:slug>/', discounts_detail, name='detail'),
    path('', discounts_list, name='list'),
]
