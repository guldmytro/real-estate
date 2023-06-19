from django.urls import path
from .views import managers_detail, managers_list


app_name = 'managers'

urlpatterns = [
    path('<int:id>/', managers_detail, name='detail'),
    path('', managers_list, name='list')
]