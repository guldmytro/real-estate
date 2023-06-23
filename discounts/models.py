from news.models import PostModel
from django.urls import reverse
from django.db import models


class Discount(PostModel):
    excerpt = models.TextField(verbose_name='Короткий опис', max_length=300)
    
    def get_absolute_url(self):
        return reverse('discounts:detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = 'Акція'
        verbose_name_plural = 'Акції'
    
