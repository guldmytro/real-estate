from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField


class Analytic(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title')),
        body=RichTextUploadingField(verbose_name=_('Text'))
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    thumbnail = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name=_('Image'))

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = _('Analytical review')
        verbose_name_plural = _('Analytical reviews')
    
    def get_absolute_url(self):
        return reverse('analytics:detail', kwargs={'id': self.id})