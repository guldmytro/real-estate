# Generated by Django 4.2.1 on 2023-06-30 09:26

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_alter_analytic_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analytic',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст'),
        ),
    ]
