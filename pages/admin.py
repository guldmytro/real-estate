from django.contrib import admin
from .models import About, AboutItem, Abroad, AbroadItem
from solo.admin import SingletonModelAdmin



class AboutItemInlineAdmin(admin.TabularInline):
    model = AboutItem


@admin.register(About)
class AboutAdmin(SingletonModelAdmin):
    list_display = ['title_1']
    inlines = [AboutItemInlineAdmin]


class AbroadItemInlineAdmin(admin.StackedInline):
    extra = 1
    model = AbroadItem


@admin.register(Abroad)
class AbroadAdmin(SingletonModelAdmin):
    list_display = ['title']
    inlines = [AbroadItemInlineAdmin]
