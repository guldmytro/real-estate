# Generated by Django 4.2.1 on 2023-06-04 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_country_alter_city_coordinates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='listings.country', verbose_name='Country'),
            preserve_default=False,
        ),
    ]