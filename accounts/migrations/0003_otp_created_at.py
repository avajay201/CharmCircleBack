# Generated by Django 4.2.17 on 2025-01-15 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
