# Generated by Django 4.1.5 on 2023-01-31 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccount', '0005_alter_account_profile_pic_alter_account_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='work_time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
