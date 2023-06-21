from django.contrib import admin
from .models import Vacantion, Department


@admin.register(Vacantion)
class VacantionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'created')
    list_filter = ('department', 'created')
    search_fields = ('title', 'description')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)