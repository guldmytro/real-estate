from django.contrib.gis.db import models
from urllib import request
from django.core.files.base import ContentFile
from django.contrib.gis.geos import Point
from django.urls import reverse
from managers.models import Manager
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.utils import timezone



class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='active')


class Listing(TranslatableModel):
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('archive', _('Archive')),
    ]
    CURRENCY_CHOICES = [
        ('$', 'USD ($)'),
        ('₴', 'UAH (₴)')
    ]
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='active', verbose_name=_('Status'))

    created = models.DateTimeField(default=timezone.now, verbose_name=_('Created'))
    updated = models.DateTimeField(default=timezone.now, verbose_name=_('Updated'))

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name=_('Manager'), blank=True, null=True)
    
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title'), default=''),
        description=models.TextField(verbose_name=_('Description'), blank=True, null=True),
        metros=models.TextField(verbose_name=_('Metros'), blank=True, null=True)
    )

    is_new_building = models.BooleanField(verbose_name=_('Is new building'), default=False)

    # Area
    area_total = models.PositiveSmallIntegerField(verbose_name=_('Total Area'), blank=True, null=True)
    area_living = models.PositiveSmallIntegerField(verbose_name=_('Living Area'), blank=True, null=True)
    area_kitchen = models.PositiveSmallIntegerField(verbose_name=_('Kitchen Area'), blank=True, null=True)

    # Rooms
    room_count = models.PositiveSmallIntegerField(verbose_name=_('Room Count'), blank=True, null=True)

    # Floors
    floor = models.PositiveSmallIntegerField(verbose_name=_('Floor'), blank=True, null=True)
    total_floors = models.PositiveSmallIntegerField(verbose_name=_('Total Floors'), blank=True, null=True)

    # Price
    price = models.PositiveIntegerField(verbose_name=_('Price'), blank=True, null=True)
    currency = models.CharField(max_length=1, default='$', choices=CURRENCY_CHOICES)

    # Location
    coordinates = models.PointField(default=Point(float(0), float(0)), blank=True, null=True)
    street = models.ForeignKey('Street', verbose_name=_('Street'), blank=True, null=True, on_delete=models.CASCADE,
                               related_name='listings')
    street_number = models.CharField(verbose_name=_('House Number'), blank=True, null=True, max_length=10)
    district = models.ForeignKey('District', verbose_name=_('District'), blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='listings')
    house_complex = models.ForeignKey('HouseComplex', verbose_name=_('House complex'), blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='listings')

    # Category / type / deal
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 blank=True, null=True, verbose_name=_('Category'), related_name='listings')
    realty_type = models.ForeignKey('RealtyType', on_delete=models.CASCADE, verbose_name=_('Realty type'),
                                    related_name='listings', blank=True, null=True)
    deal = models.ForeignKey('Deal', verbose_name=_('Deal'), blank=True, null=True, related_name='listings',
                             on_delete=models.CASCADE)

    video_url = models.URLField(verbose_name=_('Video'), blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Listing')
        verbose_name_plural = _('Listings')

    def __str__(self):
        return self.title

    def price_per_square(self):
        if self.price and self.area_total:
            return str(round(self.price / self.area_total)) + self.currency
        return False

    def formated_price(self):
        if self.price:
            price_str = str(self.price)
            result = ""
            for i, digit in enumerate(price_str[::-1]):
                if i > 0 and i % 3 == 0:
                    result = " " + result
                result = digit + result
            return f'{result}{self.currency}'
        return False

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            image.delete()
        super().delete(*args, **kwargs)

    def get_coordinates_lat(self):
        return str(self.coordinates.coords[1]).replace(",", ".") if self.coordinates else None

    def get_coordinates_lng(self):
        return str(self.coordinates.coords[0]).replace(",", ".") if self.coordinates else None

    def get_address_string(self):
        try:
            address = ', '.join(filter(lambda string: string != '' or string is not None,
                                [self.street.title, self.street_number, self.street.city.title])
                         )
            return address
        except:
            return ''
    
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
    
    def get_repair_value(self):
        try:
            kit = Kit.objects.get(listing__id=self.pk, attribute__slug='property_18')
            return kit.value
        except Kit.DoesNotExist:
            return False
    
    def get_absolute_url(self):
        return reverse('listings:detail', kwargs={'id': self.pk})


class TermFields(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    menu_label = models.CharField(max_length=300, verbose_name=_('Menu label'), blank=True, null=True)
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['slug'])
        ]
        ordering = ['slug']


class Category(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title')),
        menu_label=models.CharField(max_length=300, verbose_name=_('Menu label'), blank=True, null=True)
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class RealtyType(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title')),
        menu_label=models.CharField(max_length=300, verbose_name=_('Menu label'), blank=True, null=True)
    )

    def get_absolute_url(self):
        return f"{reverse('listings:list')}?realty_type={self.id}"
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _('Realty Type')
        verbose_name_plural = _('Realty Types')


class Deal(TermFields):

    def __str__(self):
        return self.title.capitalize()

    class Meta:
        verbose_name = _('Deal')
        verbose_name_plural = _('Deals')


class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name=_('Listing'), related_name='images')
    file = models.ImageField(upload_to='listings/%Y/%m/%d', verbose_name=_('File'), blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, verbose_name=_('Image url'))

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


class Attribute(TranslatableModel):
    BLACKLIST_ATTRIBUTES = [
        'property_56',
        'property_71', # video
        'property_80',
        'property_82',
        'property_83',
    ]
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title'))
    )
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        return self.title


class Kit(TranslatableModel):
    listing = models.ManyToManyField(Listing, verbose_name=_('Listing'),
                                     related_name='kits')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name=_('Attribute'),
                                  related_name='kits')
    translations = TranslatedFields(
        value=models.CharField(max_length=255, verbose_name=_('Value'))
    )
    untranslated_value = models.CharField(max_length=255)

    class Meta:
        ordering = ('attribute__translations__title',)
        verbose_name = _('Kit')
        verbose_name_plural = _('Kits')

    def __str__(self):
        return f'{self.value.capitalize()}'


class Country(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_('Country'), unique=True)
    )
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Region(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_('Region'), unique=True)
    )
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')


class City(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('City'))
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('Region'),
                               blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('listings:list') + f'?city={self.id}'

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class District(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_('District'))
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('City'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')


class HouseComplex(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name=_('House Complex'))
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('City'))
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('House Complex')
        verbose_name_plural = _('House Complexes')


class Street(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Street'))
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='streets', verbose_name=_('City'))

    def __str__(self):
        return f'{self.city.country.title}, {self.city.title}, {self.title}'

    class Meta:
        verbose_name = _('Street')
        verbose_name_plural = _('Streets')
