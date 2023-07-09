from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField 


class Discount(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title')),
        slug=models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True),
        body=RichTextUploadingField(verbose_name=_('Text')),
        excerpt=models.TextField(verbose_name=_('Short description'), max_length=300)
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    thumbnail = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name=_('Image'))
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')
    
    def get_absolute_url(self):
        return reverse('discounts:detail', kwargs={'slug': self.slug})