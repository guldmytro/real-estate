from django.urls import path
from .views import vacantions_list, vacantions_page

app_name = 'vacantions'

urlpatterns = [
    path('list/', vacantions_list, name='list'),
    path('', vacantions_page, name='page'),
]
