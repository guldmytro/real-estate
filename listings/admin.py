from .models import Listing, Image, Country, City, Street, Kit, Attribute, RealtyType, Category
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from parler.admin import TranslatableAdmin


class ImageInline(admin.StackedInline):
    model = Image


@admin.register(RealtyType)
class RealtyTypeAdmin(TranslatableAdmin):
    list_display = ('title', 'menu_label')


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('title', 'menu_label')      


@admin.register(Country)
class CountryAdmin(TranslatableAdmin):
    list_display = ('title',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('title',)


class KitInline(admin.StackedInline):
    model = Listing.kits.through

    readonly_fields = ['get_attribute_title']  # Add the custom method as a readonly field

    def get_attribute_title(self, obj):
        return obj.kit.attribute.title

    get_attribute_title.short_description = 'Attribute'

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if 'get_attribute_title' in fields:
            fields.remove('get_attribute_title')
            fields.insert(0, 'get_attribute_title')
        return fields


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    inlines = [KitInline]
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
    inlines = [ImageInline, KitInline]
