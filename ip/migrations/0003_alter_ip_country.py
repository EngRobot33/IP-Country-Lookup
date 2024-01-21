# Generated by Django 5.0.1 on 2024-01-17 22:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip', '0002_remove_country_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ips', to='ip.country', verbose_name='country'),
        ),
    ]