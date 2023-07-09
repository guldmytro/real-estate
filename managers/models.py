from django.db import models
import re
from urllib import request
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Manager(models.Model):
    full_name = models.CharField(max_length=255, verbose_name=_('Name'), db_index=True)
    image = models.ImageField(upload_to='managers/%Y/%m/%d', blank=True, null=True, verbose_name=_('Image'))
    image_url = models.URLField(verbose_name=_('Image url'), blank=True, null=True)

    email = models.EmailField(max_length=255, verbose_name=_('Email'), blank=True, null=True)

    experience = models.CharField(max_length=30, verbose_name=_('Experience'), blank=True, null=True)
    has_car = models.BooleanField(default=False, verbose_name=_('Has Car?'))
    about = models.TextField(verbose_name=_('About'), blank=True, null=True)

    class Meta:
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')

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
    phone = models.CharField(max_length=50, verbose_name=_('Phone'))
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='phones', verbose_name=_('Manager'))

    def __str__(self):
        return self.phone

    def clean_phone(self):
        pattern = r'\D+'
        result = re.sub(pattern, '', str(self.phone))
        return result

    class Meta:
        verbose_name = _('Phone')
        verbose_name_plural = _('Phones')
        unique_together = (
            ('phone', 'manager')
        )


class Review(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5,
                                              verbose_name=_('Rating'), choices=RATING_CHOICES)
    author = models.CharField(verbose_name=_('Author'))
    body = models.TextField(verbose_name=_('Review'), max_length=250)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    manager = models.ForeignKey(Manager, verbose_name=_('Manager'), on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.manager.full_name} - {self.author}'

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')

