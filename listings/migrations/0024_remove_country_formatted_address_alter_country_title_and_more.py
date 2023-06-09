# Generated by Django 4.2.1 on 2023-06-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0023_alter_street_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='formatted_address',
        ),
        migrations.AlterField(
            model_name='country',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Country'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('title', 'country')},
        ),
        migrations.AlterUniqueTogether(
            name='street',
            unique_together={('title', 'city')},
        ),
        migrations.RemoveField(
            model_name='city',
            name='formatted_address',
        ),
        migrations.RemoveField(
            model_name='street',
            name='formatted_address',
        ),
    ]
