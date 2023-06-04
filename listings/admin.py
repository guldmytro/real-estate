from .models import Listing, Kit, Image, City, Street
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin


class KitInline(admin.StackedInline):
    model = Kit


class ImageInline(admin.StackedInline):
    model = Image


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Listing)
class ListingAdmin(LeafletGeoAdmin):
    list_display = ('title', 'status', 'is_new_building', 'created', 'updated')
    list_editable = ('status',)
    list_filter = ('status', 'is_new_building', 'created', 'updated',)
    inlines = [ImageInline, KitInline]


