from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration
from parler.admin import TranslatableAdmin


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass
