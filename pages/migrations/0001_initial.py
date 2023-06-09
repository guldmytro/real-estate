# Generated by Django 4.2.1 on 2023-06-19 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_1', models.CharField(max_length=255, verbose_name='Заголовок 1 секції')),
                ('description_1', models.TextField(max_length=300, verbose_name='Опис 1 секції')),
                ('title_2', models.CharField(max_length=255, verbose_name='Заголовок 2 секції')),
                ('description_2', models.TextField(max_length=300, verbose_name='Опис 2 секції')),
            ],
            options={
                'verbose_name': 'Про нас',
                'verbose_name_plural': 'Про нас',
            },
        ),
        migrations.CreateModel(
            name='AboutItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(max_length=500, verbose_name='Опис')),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Порядок')),
                ('about', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pages.about')),
            ],
            options={
                'verbose_name': 'Про нас деталь',
                'verbose_name_plural': 'Про нас деталі',
                'ordering': ('order',),
            },
        ),
    ]
