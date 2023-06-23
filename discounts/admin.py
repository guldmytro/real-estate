from django.contrib import admin
from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created']
    list_filter = ['created']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created']