# Generated by Django 4.2.1 on 2023-06-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_vacantionpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacantionpage',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='vacantions/%Y/%m/%d', verbose_name='Video'),
        ),
    ]
