# Generated by Django 4.2.1 on 2023-08-14 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0043_listingtranslation_district_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingtranslation',
            name='district',
        ),
        migrations.RemoveField(
            model_name='listingtranslation',
            name='housing_complex',
        ),
        migrations.RemoveField(
            model_name='listingtranslation',
            name='metro',
        ),
    ]
