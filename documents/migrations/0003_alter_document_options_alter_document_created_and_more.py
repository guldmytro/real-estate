# Generated by Django 4.2.1 on 2023-07-09 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_document_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ('-created',), 'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterField(
            model_name='document',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='documents/%Y/%m/%d', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(verbose_name='Title'),
        ),
    ]