# Generated by Django 4.2.1 on 2023-06-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacantion',
            name='salary',
            field=models.CharField(default=0, max_length=30, verbose_name='Зарплата'),
            preserve_default=False,
        ),
    ]
