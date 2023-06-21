from django.urls import path
from .views import vacantions_list

app_name = 'vacantions'

urlpatterns = [
    path('', vacantions_list, name='list'),
]
