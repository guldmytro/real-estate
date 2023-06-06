from django.db import models
import re
from urllib import request
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Manager(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='Name', db_index=True)
    image = models.ImageField(upload_to='managers/%Y/%m/%d', blank=True, null=True)
    image_url = models.URLField(verbose_name='Image url', blank=True, null=True)

    email = models.EmailField(max_length=255, verbose_name='Email', blank=True, null=True)

    experience = models.CharField(max_length=30, verbose_name='Experience', blank=True, null=True)
    has_car = models.BooleanField(default=False, verbose_name='Has Car?')
    about = models.TextField(verbose_name='About', blank=True, null=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            try:
                res = request.urlopen(str(self.image_url))
                name = str(self.image_url).rsplit('/', 1)[1]
                self.image.save(name, ContentFile(res.read()))
            except:
                raise Exception("Sorry, I couldn't download the image")
        return super(Manager, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('managers:detail', kwargs={'id': self.pk})


class Phone(models.Model):
    phone = models.CharField(max_length=50, verbose_name='Phone')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='phones')

    def __str__(self):
        return self.phone

    def clean_phone(self):
        pattern = r'\D+'
        result = re.sub(pattern, '', str(self.phone))
        return result

    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'
        unique_together = (
            ('phone', 'manager')
        )


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5,
                                              verbose_name='Rating')
    author = models.CharField(verbose_name='Author')
    body = models.TextField(verbose_name='Review', max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(Manager, verbose_name='Manager', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.manager.full_name} - {self.author}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

