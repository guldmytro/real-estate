# Generated by Django 4.2.1 on 2023-07-25 07:13

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0040_region_city_region_regiontranslation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, default=django.contrib.gis.geos.point.Point(0.0, 0.0), null=True, srid=4326),
        ),
    ]