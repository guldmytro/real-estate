# Generated by Django 4.2.1 on 2023-06-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('body', models.TextField(verbose_name='Текст')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('thumbnail', models.ImageField(upload_to='news/%Y/%m/%d', verbose_name='Image')),
                ('excerpt', models.TextField(max_length=300, verbose_name='Короткий опис')),
            ],
            options={
                'verbose_name': 'Знижки',
                'verbose_name_plural': 'Знижка',
            },
        ),
    ]
