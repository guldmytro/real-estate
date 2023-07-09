from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Document(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_('Title')),
    )

    file = models.FileField(verbose_name=_('File'), upload_to='documents/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    
    class Meta:
        ordering = ('-created',)
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

