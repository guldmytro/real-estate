# Generated by Django 4.2.1 on 2023-07-09 12:03

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_contact_office_1_uk_contact_office_2_uk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='about_uk',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='About us section'),
        ),
        migrations.AddField(
            model_name='home',
            name='title_uk',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Title'),
        ),
    ]