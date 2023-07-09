from django.contrib import admin
from .models import Discount
from django.db import models
from ckeditor.widgets import CKEditorWidget
from parler.admin import TranslatableAdmin


@admin.register(Discount)
class DiscountAdmin(TranslatableAdmin):
    list_display = ['title', 'created']
    list_filter = ['created']
    search_fields = ['title', 'body']
    ordering = ['-created']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }