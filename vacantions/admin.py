from django.contrib import admin
from .models import Vacantion, Department
from parler.admin import TranslatableAdmin


@admin.register(Vacantion)
class VacantionAdmin(TranslatableAdmin):
    list_display = ('title', 'department', 'created')
    list_filter = ('department', 'created')
    search_fields = ('title', 'description')


@admin.register(Department)
class DepartmentAdmin(TranslatableAdmin):
    list_display = ('title',)
    search_fields = ('title',)