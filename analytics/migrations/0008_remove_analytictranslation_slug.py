# Generated by Django 4.2.1 on 2023-07-09 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_analytictranslation_alter_analytic_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analytictranslation',
            name='slug',
        ),
    ]
