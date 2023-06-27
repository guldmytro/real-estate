from django.urls import path
from .views import feadback, apply, manager_quick_message, manager_add_review, \
    seller_quick_message

app_name = 'emails'

urlpatterns = [
    path('apply/', apply, name='apply'),
    path('feadback/', feadback, name='feadback'),
    path('managers/<int:id>/add-review/', manager_add_review, name='manager_add_review'),
    path('managers/<int:id>/message/', manager_quick_message, name='manager_quick_message'),
    path('sellers/quick-message/', seller_quick_message, name='seller_quick_message')
]