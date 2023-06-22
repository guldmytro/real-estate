from django.urls import path
from .views import about, abroad_properties, contacts, course


app_name = 'pages'


urlpatterns = [
    path('abroad-properties/', abroad_properties, name='abroad_properties'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('course/', course, name='course')
]