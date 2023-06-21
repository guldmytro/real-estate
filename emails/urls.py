from django.urls import path
from .views import feadback, apply

app_name = 'emails'

urlpatterns = [
    path('apply/', apply, name='apply'),
    path('feadback/', feadback, name='feadback'),
]