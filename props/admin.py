from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, Feed


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    fields = (
        ('site_name_en', 'site_name_uk'),
        ('google_api_key'),
        ('azure_secret_key', 'azure_location'),
        ('email'),
    )


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('feed_url',)