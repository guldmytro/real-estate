from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


class PostModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    body = RichTextUploadingField(verbose_name=_('Text'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    thumbnail = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name=_('Image'))

    class Meta:
        abstract = True
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.title    


class News(PostModel):
    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def get_archive_url(self):
        return reverse('news:list')
    