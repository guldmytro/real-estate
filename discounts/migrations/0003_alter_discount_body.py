# Generated by Django 4.2.1 on 2023-06-30 08:49

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0002_alter_discount_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name='Текст'),
        ),
    ]
