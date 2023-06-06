from django.contrib import admin
from .models import Manager, Phone, Review


class PhoneInline(admin.StackedInline):
    model = Phone


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    inlines = [PhoneInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'manager', 'created')
    list_filter = ('manager__full_name', 'created')
