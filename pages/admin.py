from django.contrib import admin
from .models import About, AboutItem, Abroad, AbroadItem,\
      Contact, Course, VacantionPage, Home
from solo.admin import SingletonModelAdmin


class AboutItemInlineAdmin(admin.StackedInline):
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


@admin.register(Contact)
class ContactAdmin(SingletonModelAdmin):
    list_display = ['phone_1']


@admin.register(Course)
class CourseAdmin(SingletonModelAdmin):
    list_display = ['register_link']


@admin.register(VacantionPage)
class VacantionPageAdmin(SingletonModelAdmin):
    list_display = ['video']


@admin.register(Home)
class HomeAdmin(SingletonModelAdmin):
    list_display = ['id']
