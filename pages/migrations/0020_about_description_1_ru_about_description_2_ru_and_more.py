# Generated by Django 4.2.1 on 2024-01-07 12:32

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_alter_home_about_alter_home_about_uk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='description_1_ru',
            field=models.TextField(default='ru', max_length=300, verbose_name='Description 1 of the section (Russian)'),
        ),
        migrations.AddField(
            model_name='about',
            name='description_2_ru',
            field=models.TextField(default='ru', max_length=300, verbose_name='Description 2 of the section (Russian)'),
        ),
        migrations.AddField(
            model_name='about',
            name='title_1_ru',
            field=models.CharField(default='ru', max_length=255, verbose_name='Title 1 of the section (Russian)'),
        ),
        migrations.AddField(
            model_name='about',
            name='title_2_ru',
            field=models.CharField(default='ru', max_length=255, verbose_name='Title 2 of the section (Russian)'),
        ),
        migrations.AddField(
            model_name='aboutitem',
            name='description_ru',
            field=models.TextField(default='ru', max_length=500, verbose_name='Description (Russian)'),
        ),
        migrations.AddField(
            model_name='aboutitem',
            name='title_ru',
            field=models.CharField(default='ru', max_length=100, verbose_name='Title (Russian)'),
        ),
        migrations.AddField(
            model_name='abroad',
            name='description_ru',
            field=models.TextField(default='ru', max_length=300, verbose_name='Description (Russian)'),
        ),
        migrations.AddField(
            model_name='abroad',
            name='title_ru',
            field=models.CharField(default='ru', max_length=255, verbose_name='Title (Russian)'),
        ),
        migrations.AddField(
            model_name='abroaditem',
            name='description_ru',
            field=models.TextField(default='ru', max_length=500, verbose_name='Description (Russian)'),
        ),
        migrations.AddField(
            model_name='abroaditem',
            name='title_ru',
            field=models.CharField(default='ru', max_length=100, verbose_name='Title (Russian)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='office_1_ru',
            field=models.CharField(default='ru', max_length=255, verbose_name='Office 1 (Russian)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='office_2_ru',
            field=models.CharField(default='ru', max_length=255, verbose_name='Office 2 (Russian)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='office_3_ru',
            field=models.CharField(default='ru', max_length=255, verbose_name='Office 3 (Russian)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='schedule_ru',
            field=models.CharField(default='ru', max_length=255, verbose_name='Schedule (Russian)'),
        ),
        migrations.AddField(
            model_name='home',
            name='about_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='About us section (Russian)'),
        ),
        migrations.AddField(
            model_name='home',
            name='title_ru',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Title (Russian)'),
        ),
    ]
