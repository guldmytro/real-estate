# Generated by Django 4.2.1 on 2023-07-09 09:49

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('props', '0006_alter_siteconfiguration_site_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='site_name',
        ),
        migrations.CreateModel(
            name='SiteConfigurationTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('site_name', models.CharField(default='Contract Real Estate', max_length=255, verbose_name='Site name')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='props.siteconfiguration')),
            ],
            options={
                'verbose_name': 'Site Configuration Translation',
                'db_table': 'props_siteconfiguration_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]
