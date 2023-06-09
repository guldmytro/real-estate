# Generated by Django 4.2.1 on 2023-07-09 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('props', '0007_remove_siteconfiguration_site_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='site_name_en',
            field=models.CharField(default='Contract Real Estate', max_length=255, verbose_name='Site name (English)'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='site_name_uk',
            field=models.CharField(default='Контракт нерухомість', max_length=255, verbose_name='Site name (Ukraininan)'),
        ),
        migrations.DeleteModel(
            name='SiteConfigurationTranslation',
        ),
    ]
