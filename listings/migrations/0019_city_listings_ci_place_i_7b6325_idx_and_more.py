# Generated by Django 4.2.1 on 2023-06-10 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0018_rename_house_num_listing_street_number_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='city',
            index=models.Index(fields=['place_id'], name='listings_ci_place_i_7b6325_idx'),
        ),
        migrations.AddIndex(
            model_name='country',
            index=models.Index(fields=['place_id'], name='listings_co_place_i_b204c7_idx'),
        ),
        migrations.AddIndex(
            model_name='street',
            index=models.Index(fields=['place_id'], name='listings_st_place_i_4824b4_idx'),
        ),
    ]