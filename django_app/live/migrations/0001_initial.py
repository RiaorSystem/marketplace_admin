# Generated by Django 5.1.6 on 2025-03-20 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LiveStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('viewers_count', models.PositiveIntegerField(default=0)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
