from django.urls import path
from .views import analytics_list, analytics_detail

app_name = 'analytics'

urlpatterns = [
    path('<int:id>/', analytics_detail, name='detail'),
    path('', analytics_list, name='list'),
]
