# Generated by Django 5.1.6 on 2025-03-01 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escrow', '0003_advertisementapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='duration',
            field=models.IntegerField(help_text='Duration in days'),
        ),
    ]
