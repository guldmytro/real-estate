from django.contrib import admin
from .models import Manager, Phone, Review
from parler.admin import TranslatableAdmin


class PhoneInline(admin.StackedInline):
    model = Phone


@admin.register(Manager)
class ManagerAdmin(TranslatableAdmin):
    list_display = ('full_name', 'email')
    inlines = [PhoneInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'manager', 'created')
