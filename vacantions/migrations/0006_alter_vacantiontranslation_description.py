# Generated by Django 4.2.1 on 2024-02-23 08:24

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacantions', '0005_alter_vacantion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacantiontranslation',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, verbose_name='Description'),
        ),
    ]
