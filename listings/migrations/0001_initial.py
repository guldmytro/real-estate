# Generated by Django 4.2.1 on 2023-06-03 05:05

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RealtyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('archive', 'Archive')], default='active', max_length=7, verbose_name='Status')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_new_building', models.BooleanField(default=False, verbose_name='Is new building')),
                ('area_total', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Total Area')),
                ('area_living', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Living Area')),
                ('area_kitchen', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Kitchen Area')),
                ('room_count', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Room Count')),
                ('floor', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Floor')),
                ('total_floors', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Total Floors')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Price')),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='listings.category', verbose_name='Category')),
                ('realty_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='listings.realtytype', verbose_name='Realty type')),
            ],
            options={
                'verbose_name': 'Listing',
                'verbose_name_plural': 'Listings',
                'ordering': ('-created',),
            },
            managers=[
                ('active', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.attribute', verbose_name='Attribute')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing', verbose_name='Listing')),
            ],
            options={
                'verbose_name': 'Kit',
                'verbose_name_plural': 'Kits',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='listings/%Y/%m/%d')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='listings.listing')),
            ],
        ),
    ]
