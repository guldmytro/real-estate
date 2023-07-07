from django.db import models
from solo.models import SingletonModel
from django.utils.translation import gettext_lazy as _


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Contract Real Estate', verbose_name=_('Site name'))
    google_api_key = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('API-key for Google Maps'))
    crm_api = models.URLField(verbose_name=_('CRM-feed for parsing'), null=True, blank=True)
    email = models.EmailField(verbose_name=_('Email'), default='example@mail.com')

    def __str__(self):
        return _('Site Configuration')

    class Meta:
        verbose_name = _('Site Configuration')
