# Generated by Django 4.2.1 on 2023-06-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_rename_news_analytic_alter_analytic_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analytic',
            name='body',
            field=models.TextField(verbose_name='Текст'),
        ),
    ]