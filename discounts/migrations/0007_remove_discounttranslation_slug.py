# Generated by Django 4.2.1 on 2023-07-09 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0006_discounttranslation_alter_discount_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discounttranslation',
            name='slug',
        ),
    ]
