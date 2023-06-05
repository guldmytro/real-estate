from django.urls import path
from .views import managers_detail


app_name = 'managers'

urlpatterns = [
    path('<int:id>/', managers_detail, name='detail'),
]