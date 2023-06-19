from django.urls import path
from .views import about, abroad_properties


app_name = 'pages'


urlpatterns = [
    path('abroad-properties/', abroad_properties, name='abroad_properties'),
    path('about/', about, name='about')
]