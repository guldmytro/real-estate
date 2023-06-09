# Generated by Django 4.2.1 on 2023-07-11 10:19

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0037_remove_category_menu_label_remove_category_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realtytype',
            name='menu_label',
        ),
        migrations.RemoveField(
            model_name='realtytype',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='realtytype',
            name='title',
        ),
        migrations.CreateModel(
            name='RealtyTypeTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('menu_label', models.CharField(blank=True, max_length=300, null=True, verbose_name='Menu label')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='listings.realtytype')),
            ],
            options={
                'verbose_name': 'Realty Type Translation',
                'db_table': 'listings_realtytype_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]
