from django.db import models
from django.urls import reverse


class PostModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    thumbnail = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name='Image')

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
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
