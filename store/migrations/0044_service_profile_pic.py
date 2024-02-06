# Generated by Django 4.1.6 on 2023-02-16 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0043_alter_enquiry_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='profile_pic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='store.profilepic'),
        ),
    ]
