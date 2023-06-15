# Generated by Django 4.2.1 on 2023-06-10 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0019_city_listings_ci_place_i_7b6325_idx_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='coordinates',
        ),
        migrations.AlterField(
            model_name='city',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='country',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='street',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Street'),
        ),
    ]