# Generated by Django 4.2.1 on 2023-06-02 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('props', '0002_siteconfiguration_google_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='crm_api',
            field=models.URLField(blank=True, null=True, verbose_name='CRM-feed для парсингу'),
        ),
    ]
