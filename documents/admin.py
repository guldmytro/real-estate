from django.contrib import admin
from .models import Document
from parler.admin import TranslatableAdmin


@admin.register(Document)
class DocumentAdmin(TranslatableAdmin):
    list_display = ['title', 'created']
    list_filter = ['created']
    search_fields = ['title']
    ordering = ['-created']