from django.urls import path
from .views import about, abroad_properties, contacts, course, \
    pricing, reviews, seller, home, guarantees, set_city


app_name = 'pages'


urlpatterns = [
    path('abroad-properties/', abroad_properties, name='abroad_properties'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('course/', course, name='course'),
    path('guarantees/', guarantees, name='guarantees'),
    path('pricing/', pricing, name='pricing'),
    path('reviews/', reviews, name='reviews'),
    path('seller/', seller, name='seller'),
    path('set-city/<int:pk>/', set_city, name='set-city'),
    path('', home, name='home')
]