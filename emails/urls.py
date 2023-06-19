from django.urls import path
from .views import feadback

app_name = 'emails'

urlpatterns = [
    path('feadback/', feadback, name='feadback'),
]