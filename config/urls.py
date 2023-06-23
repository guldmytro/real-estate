"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('', include('pages.urls', namespace='pages')),
    path('analytics/', include('analytics.urls', namespace='analytics')),
    path('discounts/', include('discounts.urls', namespace='discounts')),
    path('news/', include('news.urls', namespace='news')),
    path('vacantions/', include('vacantions.urls', namespace='vacantions')),
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),
    path('listings/', include('listings.urls', namespace='listings')),
    path('managers/', include('managers.urls', namespace='managers')),
    path('emails/', include('emails.urls', namespace='emails')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
