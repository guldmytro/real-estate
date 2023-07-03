from django.db import models
from solo.models import SingletonModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class About(SingletonModel):
    title_1 = models.CharField(max_length=255, verbose_name='Заголовок 1 секції')
    description_1 = models.TextField(max_length=300, verbose_name='Опис 1 секції')

    title_2 = models.CharField(max_length=255, verbose_name='Заголовок 2 секції')
    description_2 = models.TextField(max_length=300, verbose_name='Опис 2 секції')

    def __str__(self):
        return self.title_1

    def get_absolute_url(self):
        return reverse('pages:about')

    class Meta:
        verbose_name = 'Про нас'
        verbose_name_plural = 'Про нас'


class AboutItem(models.Model):
    CLASS_CHOICES = (
        ('about-item_third', '1/3'),
        ('about-item_half', '1/2'),
        ('about-item_full', '1/1'),
    )
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(max_length=500, verbose_name='Опис')
    size = models.CharField(max_length=16, verbose_name='Розмір (в колонках)', 
                            default='about-item_half', choices=CLASS_CHOICES)
    order = models.PositiveSmallIntegerField(verbose_name='Порядок', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('order',)
        verbose_name = 'Про нас деталь'
        verbose_name_plural = 'Про нас деталі'


class Abroad(SingletonModel):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(max_length=300, verbose_name='Опис')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:abroad_properties')

    class Meta:
        verbose_name = 'Нерухомість закордоном'
        verbose_name_plural = 'Нерухомість закордоном'


class AbroadItem(models.Model):
    abroad = models.ForeignKey(Abroad, on_delete=models.CASCADE, related_name='items')
    title_bg = models.CharField(max_length=15, verbose_name='Заголовок на фоні')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(max_length=500, verbose_name='Опис')
    link = models.URLField(verbose_name='Посилання')

    background_image = models.ImageField(upload_to='abroad_properties/%Y/%m/%d',
                                         verbose_name='Фон')
    photo_1 = models.ImageField(upload_to='abroad_properties/%Y/%m/%d',
                                verbose_name='Фото 1')
    photo_2 = models.ImageField(upload_to='abroad_properties/%Y/%m/%d',
                                verbose_name='Фото 2')

    order = models.PositiveSmallIntegerField(verbose_name='Порядок', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('order',)
        verbose_name = 'Нерухомість закордоном (елемент)'
        verbose_name_plural = 'Нерухомість закордоном (елемент)'


class Contact(SingletonModel):
    phone_1 = models.CharField(max_length=30, verbose_name='Телефон 1')
    phone_2 = models.CharField(max_length=30, verbose_name='Телефон 2')
    
    email = models.EmailField(verbose_name='Пошта')
    
    schedule = models.CharField(max_length=255, verbose_name='Режим роботи')
    
    office_1 = models.CharField(max_length=255, verbose_name='Офіс 1')
    office_2 = models.CharField(max_length=255, verbose_name='Офіс 2')
    office_3 = models.CharField(max_length=255, verbose_name='Офіс 3')

    telegram = models.URLField(verbose_name='Телеграм', blank=True, null=True)
    viber = models.URLField(verbose_name='Вайбер', blank=True, null=True)
    instagram = models.URLField(verbose_name='Інстаграм', blank=True, null=True)
    facebook = models.URLField(verbose_name='Фейсбук', blank=True, null=True)

    def __str__(self):
        return 'Контакти'

    def get_absolute_url(self):
        return reverse('pages:contacts')
    
    class Meta:
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'


class Course(SingletonModel):
    register_link = models.URLField(verbose_name='Зсилка на реєстрацію', blank=True, null=True)
    auth_link = models.URLField(verbose_name='Зсилка на авторизацію', blank=True, null=True)

    def __str__(self):
        return 'Курс'

    def get_absolute_url(self):
        return reverse('pages:course')
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курс'


class VacantionPage(SingletonModel):
    video = models.FileField(upload_to='vacantions/%Y/%m/%d', verbose_name='Video',
                             blank=True, null=True)
    poster = models.FileField(upload_to='vacantions/%Y/%m/%d', verbose_name='Poster',
                              blank=True, null=True)

    def __str__(self):
        return 'Вакансії'

    def get_absolute_url(self):
        return reverse('vacantions:page')
    
    class Meta:
        verbose_name = 'Вакансії'
        verbose_name_plural = 'Вакансії'


class Home(SingletonModel):
    title = models.CharField(max_length=150, verbose_name='Заголовок', null=True, blank=True)
    about = RichTextUploadingField(verbose_name='Про нас секція', null=True, blank=True)
    
    def __str__(self):
        return 'Головна'

    def get_absolute_url(self):
        return reverse('pages:home')
    
    class Meta:
        verbose_name = 'Головна'
        verbose_name_plural = 'Головна'