from news.models import PostModel
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _


class Discount(PostModel):
    excerpt = models.TextField(verbose_name=_('Short description'), max_length=300)

    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')
            
    def get_absolute_url(self):
        return reverse('discounts:detail', kwargs={'slug': self.slug})
    
    def get_archive_url(self):
        return reverse('discounts:list')
    
