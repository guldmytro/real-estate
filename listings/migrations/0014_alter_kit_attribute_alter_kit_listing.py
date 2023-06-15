# Generated by Django 4.2.1 on 2023-06-06 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0013_alter_phone_unique_together_remove_phone_manager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kit',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kits', to='listings.attribute', verbose_name='Attribute'),
        ),
        migrations.AlterField(
            model_name='kit',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kits', to='listings.listing', verbose_name='Listing'),
        ),
    ]