# Generated by Django 5.1.6 on 2025-03-20 10:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('escrow', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='advertisementapplication',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='escrow.advertisement'),
        ),
        migrations.AddField(
            model_name='advertisementapplication',
            name='advertiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_applied', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='escrow',
            name='advertisement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='escrow', to='escrow.advertisement'),
        ),
        migrations.AddField(
            model_name='escrow',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='escrows_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='escrow',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escrows_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='escrowwallet',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escrow_wallet', to=settings.AUTH_USER_MODEL),
        ),
    ]
