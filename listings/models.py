from django.contrib.gis.db import models
from urllib import request
from django.core.files.base import ContentFile
from django.contrib.gis.geos import Point


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='active')


class Listing(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archive', 'Archive'),
    ]
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='active', verbose_name='Status')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')

    title = models.CharField(max_length=255, verbose_name='Title', default='')
    description = models.TextField(verbose_name='Description', blank=True, null=True)

    is_new_building = models.BooleanField(verbose_name='Is new building', default=False)

    # Area
    area_total = models.PositiveSmallIntegerField(verbose_name='Total Area', blank=True, null=True)
    area_living = models.PositiveSmallIntegerField(verbose_name='Living Area', blank=True, null=True)
    area_kitchen = models.PositiveSmallIntegerField(verbose_name='Kitchen Area', blank=True, null=True)

    # Rooms
    room_count = models.PositiveSmallIntegerField(verbose_name='Room Count', blank=True, null=True)

    # Floors
    floor = models.PositiveSmallIntegerField(verbose_name='Floor', blank=True, null=True)
    total_floors = models.PositiveSmallIntegerField(verbose_name='Total Floors', blank=True, null=True)

    # Price
    price = models.PositiveIntegerField(verbose_name='Price', blank=True, null=True)

    coordinates = models.PointField(default=Point(float(0), float(0)))

    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 blank=True, null=True, verbose_name='Category', related_name='listings')
    realty_type = models.ForeignKey('RealtyType', on_delete=models.CASCADE, verbose_name='Realty type',
                                    related_name='listings', blank=True, null=True)

    active = ActiveManager()
    objects = models.Manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        for image in self.images:
            image.delete()
        super().delete(*args, **kwargs)


class TermFields(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, verbose_name='Slug')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Category(TermFields):
    pass


class RealtyType(TermFields):
    pass


class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='listings/%Y/%m/%d', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image_url and not self.file:
            try:
                res = request.urlopen(str(self.image_url))
                name = str(self.image_url).rsplit('/', 1)[1]
                self.file.save(name, ContentFile(res.read()))
            except:
                raise Exception("Sorry, I couldn't download the image")
        return super(Image, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('listing', 'image_url')
        )






class Attribute(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'

    def __str__(self):
        return self.title


class Kit(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name='Listing')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Attribute')
    value = models.CharField(max_length=255, verbose_name='Value')

    class Meta:
        verbose_name = 'Kit'
        verbose_name_plural = 'Kits'

    def __str__(self):
        return f'{self.attribute.title} - {self.value}'
