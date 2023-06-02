from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Contract Real Estate')
    google_api_key = models.CharField(max_length=255, null=True, blank=True, verbose_name='API-key for Google Maps')
    crm_api = models.URLField(verbose_name='CRM-feed for parsing', null=True, blank=True)

    def __str__(self):
        return 'Site Configuration'

    class Meta:
        verbose_name = 'Site Configuration'
