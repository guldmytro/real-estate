from .models import Listing, Kit, Image
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin


class KitInline(admin.StackedInline):
    model = Kit


class ImageInline(admin.StackedInline):
    model = Image


@admin.register(Listing)
class ListingAdmin(LeafletGeoAdmin):
    list_display = ('title', 'status', 'is_new_building', 'created', 'updated')
    list_editable = ('status',)
    list_filter = ('status', 'is_new_building', 'created', 'updated',)
    inlines = [ImageInline, KitInline]


