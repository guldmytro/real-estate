from django.db import models
from solo.models import SingletonModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class About(SingletonModel):
    title_1 = models.CharField(max_length=255, verbose_name=_('Title 1 of the section (English)'))
    title_1_uk = models.CharField(max_length=255, verbose_name=_('Title 1 of the section (Ukrainian)'))
    title_1_ru = models.CharField(max_length=255, verbose_name=_('Title 1 of the section (Russian)'), default='ru')
    description_1 = models.TextField(max_length=300, verbose_name=_('Description 1 of the section (English)'))
    description_1_uk = models.TextField(max_length=300, verbose_name=_('Description 1 of the section (Ukrainian)'))
    description_1_ru = models.TextField(max_length=300, verbose_name=_('Description 1 of the section (Russian)'), default='ru')

    title_2 = models.CharField(max_length=255, verbose_name=_('Title 2 of the section (English)'))
    title_2_uk = models.CharField(max_length=255, verbose_name=_('Title 2 of the section (Ukrainian)'))
    title_2_ru = models.CharField(max_length=255, verbose_name=_('Title 2 of the section (Russian)'), default='ru')

    description_2 = models.TextField(max_length=300, verbose_name=_('Description 2 of the section (English)'))
    description_2_uk = models.TextField(max_length=300, verbose_name=_('Description 2 of the section (Ukrainian)'))
    description_2_ru = models.TextField(max_length=300, verbose_name=_('Description 2 of the section (Russian)'), default='ru')

    def __str__(self):
        return self.title_1

    def get_absolute_url(self):
        return reverse('pages:about')

    class Meta:
        verbose_name = _('About us')
        verbose_name_plural = _('About us')


class AboutItem(models.Model):
    CLASS_CHOICES = (
        ('about-item_third', '1/3'),
        ('about-item_half', '1/2'),
        ('about-item_full', '1/1'),
    )
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='items', verbose_name=_('About us'))
    title = models.CharField(max_length=100, verbose_name=_('Title (English)'))
    title_uk = models.CharField(max_length=100, verbose_name=_('Title (Ukrainian)'))
    title_ru = models.CharField(max_length=100, verbose_name=_('Title (Russian)'), default='ru')
    description = models.TextField(max_length=500, verbose_name=_('Description (English)'))
    description_uk = models.TextField(max_length=500, verbose_name=_('Description (Ukrainian)'))
    description_ru = models.TextField(max_length=500, verbose_name=_('Description (Russian)'), default='ru')

    size = models.CharField(max_length=16, verbose_name=_('Column size'), 
                            default='about-item_half', choices=CLASS_CHOICES)
    order = models.PositiveSmallIntegerField(verbose_name=_('Order'), null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('order',)
        verbose_name = _('About us detail')
        verbose_name_plural = _('About us details')


class Abroad(SingletonModel):
    title = models.CharField(max_length=255, verbose_name=_('Title (English)'))
    title_uk = models.CharField(max_length=255, verbose_name=_('Title (Ukrainian)'), default='uk')
    title_ru = models.CharField(max_length=255, verbose_name=_('Title (Russian)'), default='ru')

    description = models.TextField(max_length=300, verbose_name=_('Description (English)'))
    description_uk = models.TextField(max_length=300, verbose_name=_('Description (Ukrainian)'), default='uk')
    description_ru = models.TextField(max_length=300, verbose_name=_('Description (Russian)'), default='ru')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:abroad_properties')

    class Meta:
        verbose_name = _('Real estate abroad')
        verbose_name_plural = _('Real estate abroad')


class AbroadItem(models.Model):
    abroad = models.ForeignKey(Abroad, on_delete=models.CASCADE, related_name='items')
    title_bg = models.CharField(max_length=15, verbose_name=_('Bg title'))
    title = models.CharField(max_length=100, verbose_name=_('Title (English)'))
    title_uk = models.CharField(max_length=100, verbose_name=_('Title (Ukrainian)'), default='uk')
    title_ru = models.CharField(max_length=100, verbose_name=_('Title (Russian)'), default='ru')
    description = models.TextField(max_length=500, verbose_name=_('Description (English)'))
    description_uk = models.TextField(max_length=500, verbose_name=_('Description (Ukrainian)'), default='uk')
    description_ru = models.TextField(max_length=500, verbose_name=_('Description (Russian)'), default='ru')
    link = models.URLField(verbose_name=_('Link'))

    background_image = models.ImageField(upload_to='abroad_properties/%Y/%m/%d',
                                         verbose_name=_('Background image'))
    photo_1 = models.ImageField(upload_to='abroad_properties/%Y/%m/%d',
                                verbose_name=_('Photo 1'))
    photo_2 = models.ImageField(upload_to='abroad_properties/%Y/%m/%d',
                                verbose_name=_('Photo 2'))

    order = models.PositiveSmallIntegerField(verbose_name=_('Order'), null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('order',)
        verbose_name = _('Real estate element')
        verbose_name_plural = _('Real estate element')


class Contact(SingletonModel):
    phone_1 = models.CharField(max_length=30, verbose_name=_('Phone 1'))
    phone_2 = models.CharField(max_length=30, verbose_name=_('Phone 2'))
    
    email = models.EmailField(verbose_name=_('Email'))
    
    schedule = models.CharField(max_length=255, verbose_name=_('Schedule (English)'))
    schedule_uk = models.CharField(max_length=255, verbose_name=_('Schedule (Ukrainian)'), default='uk')
    schedule_ru = models.CharField(max_length=255, verbose_name=_('Schedule (Russian)'), default='ru')
    
    office_1 = models.CharField(max_length=255, verbose_name=_('Office 1 (English)'))
    office_1_uk = models.CharField(max_length=255, verbose_name=_('Office 1 (Ukrainian)'), default='uk')
    office_1_ru = models.CharField(max_length=255, verbose_name=_('Office 1 (Russian)'), default='ru')

    office_2 = models.CharField(max_length=255, verbose_name=_('Office 2 (English)'))
    office_2_uk = models.CharField(max_length=255, verbose_name=_('Office 2 (Ukrainian)'), default='uk')
    office_2_ru = models.CharField(max_length=255, verbose_name=_('Office 2 (Russian)'), default='ru')
    
    office_3 = models.CharField(max_length=255, verbose_name=_('Office 3 (English)'))
    office_3_uk = models.CharField(max_length=255, verbose_name=_('Office 3 (Ukrainian)'), default='uk')
    office_3_ru = models.CharField(max_length=255, verbose_name=_('Office 3 (Russian)'), default='ru')

    telegram = models.URLField(verbose_name=_('Telegram'), blank=True, null=True)
    viber = models.URLField(verbose_name=_('Viber'), blank=True, null=True)
    instagram = models.URLField(verbose_name=_('Instagram'), blank=True, null=True)
    facebook = models.URLField(verbose_name=_('Facebook'), blank=True, null=True)

    def get_absolute_url(self):
        return reverse('pages:contacts')
    
    class Meta:
        verbose_name = _('Contacts')
        verbose_name_plural = _('Contacts')


class Course(SingletonModel):
    register_link = models.URLField(verbose_name=_('Register link'), blank=True, null=True)
    auth_link = models.URLField(verbose_name=_('Auth link'), blank=True, null=True)

    def get_absolute_url(self):
        return reverse('pages:course')
    
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Course')


class VacantionPage(SingletonModel):
    video = models.FileField(upload_to='vacantions/%Y/%m/%d', verbose_name=_('Video'),
                             blank=True, null=True)
    poster = models.FileField(upload_to='vacantions/%Y/%m/%d', verbose_name=_('Poster'),
                              blank=True, null=True)

    def get_absolute_url(self):
        return reverse('vacantions:page')
    
    class Meta:
        verbose_name = _('Vacancies')
        verbose_name_plural = _('Vacancies')


class Home(SingletonModel):
    title = models.CharField(max_length=150, verbose_name=_('Title (English)'), null=True, blank=True)
    title_uk = models.CharField(max_length=150, verbose_name=_('Title (Ukrainian)'), null=True, blank=True)
    title_ru = models.CharField(max_length=150, verbose_name=_('Title (Russian)'), null=True, blank=True)

    about = RichTextUploadingField(verbose_name=_('About us section (English)'), null=True, blank=True)
    about_uk = RichTextUploadingField(verbose_name=_('About us section (Ukrainian)'), null=True, blank=True)
    about_ru = RichTextUploadingField(verbose_name=_('About us section (Russian)'), null=True, blank=True)

    def get_absolute_url(self):
        return reverse('pages:home')
    
    class Meta:
        verbose_name = _('Home')
        verbose_name_plural = _('Home')
