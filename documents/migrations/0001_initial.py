# Generated by Django 4.2.1 on 2023-06-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='Заголовок')),
                ('file', models.FileField(upload_to='', verbose_name='Файл')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документи',
                'ordering': ('-created',),
            },
        ),
    ]
