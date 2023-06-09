# Generated by Django 4.2.1 on 2023-07-10 13:20

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0034_alter_city_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Attribute Translation',
                'db_table': 'listings_attribute_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='KitTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Kit Translation',
                'db_table': 'listings_kit_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.AlterModelOptions(
            name='kit',
            options={'ordering': ('attribute__translations__title',), 'verbose_name': 'Kit', 'verbose_name_plural': 'Kits'},
        ),
        migrations.RemoveIndex(
            model_name='kit',
            name='listings_ki_value_c9ad65_idx',
        ),
        migrations.AlterUniqueTogether(
            name='kit',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='title',
        ),
        migrations.AddField(
            model_name='kittranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='listings.kit'),
        ),
        migrations.AddField(
            model_name='attributetranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='listings.attribute'),
        ),
        migrations.RemoveField(
            model_name='kit',
            name='value',
        ),
        migrations.AlterUniqueTogether(
            name='kittranslation',
            unique_together={('language_code', 'master')},
        ),
        migrations.AlterUniqueTogether(
            name='attributetranslation',
            unique_together={('language_code', 'master')},
        ),
    ]
