from django.contrib import admin
from .models import Analytic
from django.db import models
from ckeditor.widgets import CKEditorWidget


@admin.register(Analytic)
class AnalyticAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created']
    list_filter = ['created']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }