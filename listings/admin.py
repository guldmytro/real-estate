from .models import Listing, Image, Country, City, Street, \
      Kit, Attribute, RealtyType, Category, Region
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from parler.admin import TranslatableAdmin


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1

@admin.register(RealtyType)
class RealtyTypeAdmin(TranslatableAdmin):
    list_display = ('title', 'menu_label')


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('title', 'menu_label')      


@admin.register(Country)
class CountryAdmin(TranslatableAdmin):
    list_display = ('title',)


@admin.register(Region)
class RegionAdmin(TranslatableAdmin):
    list_display = ('title',)


@admin.register(Attribute)
class AttributeAdmin(TranslatableAdmin):
    list_display = ('title',)


class KitInline(admin.StackedInline):
    model = Listing.kits.through
    extra = 1


@admin.register(Kit)
class KitAdmin(TranslatableAdmin):
    inlines = [KitInline]
    raw_id_fields = ['listing']
    exclude = ['listing']

@admin.register(City)
class CityAdmin(TranslatableAdmin):
    list_display = ('title',)


@admin.register(Street)
class StreetAdmin(TranslatableAdmin):
    list_display = ('title',)


@admin.register(Listing)
class ListingAdmin(LeafletGeoAdmin, TranslatableAdmin):
    list_display = ('title', 'status', 'is_new_building', 'created', 'updated')
    list_editable = ('status',)
    list_filter = ('status', 'manager', 'is_new_building', 'created', 'updated',)
