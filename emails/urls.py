from django.urls import path
from .views import feadback, apply, manager_quick_message, manager_add_review, \
    seller_quick_message, listing_quick_message, listing_message, listing_visit, \
    listing_credit, listing_check

app_name = 'emails'

urlpatterns = [
    path('apply/', apply, name='apply'),
    path('feadback/', feadback, name='feadback'),
    path('managers/<int:id>/add-review/', manager_add_review, name='manager_add_review'),
    path('managers/<int:id>/message/', manager_quick_message, name='manager_quick_message'),
    path('sellers/quick-message/', seller_quick_message, name='seller_quick_message'),
    path('listings/<int:id>/quick-message/', listing_quick_message, name='listing_quick_message'),
    path('listings/<int:id>/message/', listing_message, name='listing_message'),
    path('listings/<int:id>/visit/', listing_visit, name='listing_visit'),
    path('listings/<int:id>/credit/', listing_credit, name='listing_credit'),
    path('listings/<int:id>/check/', listing_check, name='listing_check'),
]