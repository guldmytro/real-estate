from django.contrib import admin
from .models import Analytic
from django.db import models
from ckeditor.widgets import CKEditorWidget
from parler.admin import TranslatableAdmin


@admin.register(Analytic)
class AnalyticAdmin(TranslatableAdmin):
    list_display = ['title', 'created']
    list_filter = ['created']
    search_fields = ['title', 'body']
    ordering = ['-created']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }