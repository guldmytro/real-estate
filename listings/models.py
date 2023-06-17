from django.contrib.gis.db import models
from urllib import request
from django.core.files.base import ContentFile
from django.contrib.gis.geos import Point
from django.urls import reverse
from managers.models import Manager


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

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='Manager', blank=True, null=True)

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

    # Location
    coordinates = models.PointField(default=Point(float(0), float(0)))
    street = models.ForeignKey('Street', verbose_name='Street', blank=True, null=True, on_delete=models.CASCADE,
                               related_name='listings')
    street_number = models.CharField(verbose_name='House Number', blank=True, null=True, max_length=10)

    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 blank=True, null=True, verbose_name='Category', related_name='listings')
    realty_type = models.ForeignKey('RealtyType', on_delete=models.CASCADE, verbose_name='Realty type',
                                    related_name='listings', blank=True, null=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        return self.title

    def price_per_square(self):
        if self.price and self.area_total:
            return round(self.price / self.area_total)
        return False

    def formated_price(self):
        if self.price:
            price_str = str(self.price)
            result = ""
            for i, digit in enumerate(price_str[::-1]):
                if i > 0 and i % 3 == 0:
                    result = " " + result
                result = digit + result
            return result
        return False

    def delete(self, *args, **kwargs):
        for image in self.images:
            image.delete()
        super().delete(*args, **kwargs)

    def get_coordinates_lat(self):
        return self.coordinates.coords[1] if self.coordinates else None

    def get_coordinates_lng(self):
        return self.coordinates.coords[0] if self.coordinates else None

    def get_address_string(self):
        return ', '.join(filter(lambda string: string != '' or string != None,
                                [self.street.title, self.street_number, self.street.city.title])
                         )
    
    def get_google_maps_link(self):
        if self.coordinates is None:
            return False
        
        base_url = "https://www.google.com/maps"
        params = {
            "saddr": "",
            "daddr": f"{self.get_coordinates_lat()},{self.get_coordinates_lng()}",  
            "directions": ""
        }
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{base_url}?{query_string}"

    def get_absolute_url(self):
        return reverse('listings:detail', kwargs={'id': self.pk})


class TermFields(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['slug'])
        ]
        ordering = ['slug']


class Category(TermFields):
    pass


class RealtyType(TermFields):
    class Meta:
        verbose_name = 'Realty Type'
        verbose_name_plural = 'Realty Types'


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
    BLACKLIST_ATTRIBUTES = [
        'property_56',
        'property_80',
        'property_82',
        'property_83',
    ]
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'

    def __str__(self):
        return self.title


class Kit(models.Model):
    listing = models.ManyToManyField(Listing, verbose_name='Listing',
                                related_name='kits')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Attribute',
                                  related_name='kits')
    value = models.CharField(max_length=255, verbose_name='Value')

    class Meta:
        unique_together = (
            ('attribute', 'value')
        )
        ordering = ('attribute__title',)
        verbose_name = 'Kit'
        verbose_name_plural = 'Kits'

    def __str__(self):
        return f'{self.value}'


class Country(models.Model):
    title = models.CharField(max_length=100, verbose_name='Country', unique=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class City(models.Model):
    title = models.CharField(max_length=255, verbose_name='City')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Country')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        unique_together = (
            ('title', 'country'),
        )

class Street(models.Model):
    title = models.CharField(max_length=255, verbose_name='Street')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='streets')

    def __str__(self):
        return f'{self.city.country.title}, {self.city.title}, {self.title}'

    class Meta:
        verbose_name = 'Street'
        verbose_name_plural = 'Streets'
        unique_together = (
            ('title', 'city'),
        )
