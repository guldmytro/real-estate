# Generated by Django 4.2.1 on 2023-06-03 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_alter_listing_realty_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('listing', 'image_url')},
        ),
    ]
