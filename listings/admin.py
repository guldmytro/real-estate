from .models import Listing, Image, Country, City, Street, Kit
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin


class ImageInline(admin.StackedInline):
    model = Image


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Kit)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')


@admin.register(City)
class CityAdmin(LeafletGeoAdmin):
    list_display = ('title',)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Listing)
class ListingAdmin(LeafletGeoAdmin):
    list_display = ('title', 'status', 'is_new_building', 'created', 'updated')
    list_editable = ('status',)
    list_filter = ('status', 'manager', 'is_new_building', 'created', 'updated',)
    inlines = [ImageInline]
