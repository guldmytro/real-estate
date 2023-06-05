# Generated by Django 4.2.1 on 2023-06-05 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0010_alter_city_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='managers/%Y/%m/%d')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.manager', verbose_name='Manager'),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50, verbose_name='Phone')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='listings.manager')),
            ],
            options={
                'verbose_name': 'Phone',
                'verbose_name_plural': 'Phones',
                'unique_together': {('phone', 'manager')},
            },
        ),
    ]
