# Generated by Django 4.2.17 on 2025-01-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_otp_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='otp_sent',
            field=models.IntegerField(default=0),
        ),
    ]
