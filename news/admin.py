from django.contrib import admin
from .models import News
from django.db import models
from ckeditor.widgets import CKEditorWidget
from parler.admin import TranslatableAdmin


@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = ['title', 'slug', 'created']
    list_filter = ['created']
    search_fields = ['title', 'body']
    ordering = ['-created']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
