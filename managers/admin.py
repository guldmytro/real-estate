from django.contrib import admin
from .models import Manager, Phone


class PhoneInline(admin.StackedInline):
    model = Phone


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    inlines = [PhoneInline]