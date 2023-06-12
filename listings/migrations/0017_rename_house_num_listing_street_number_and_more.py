# Generated by Django 4.2.1 on 2023-06-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0016_listing_house_num'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='street',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='city',
            name='place_id',
            field=models.CharField(default=12, max_length=255, verbose_name='Place id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='place_id',
            field=models.CharField(default=12, max_length=255, verbose_name='Place id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='street',
            name='place_id',
            field=models.CharField(default=12, max_length=255, verbose_name='Place id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='country',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Country'),
        ),
    ]
