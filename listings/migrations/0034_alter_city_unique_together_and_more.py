# Generated by Django 4.2.1 on 2023-07-10 12:28

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0033_remove_country_title_countrytranslation'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='street',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='city',
            name='title',
        ),
        migrations.RemoveField(
            model_name='street',
            name='title',
        ),
        migrations.CreateModel(
            name='StreetTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=255, verbose_name='Street')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='listings.street')),
            ],
            options={
                'verbose_name': 'Street Translation',
                'db_table': 'listings_street_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='CityTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=255, verbose_name='City')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='listings.city')),
            ],
            options={
                'verbose_name': 'City Translation',
                'db_table': 'listings_city_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]
