# Generated by Django 4.1.5 on 2023-01-31 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccount', '0007_remove_account_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='more_photos',
            field=models.ImageField(blank=True, default='', null=True, upload_to='mediafiles'),
        ),
        migrations.AddField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(blank=True, default='', null=True, upload_to='mediafiles'),
        ),
    ]
