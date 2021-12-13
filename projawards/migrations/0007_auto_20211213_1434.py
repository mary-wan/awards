# Generated by Django 2.2.24 on 2021-12-13 11:34

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('projawards', '0006_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='contact',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=phone_field.models.PhoneField(blank=True, max_length=15),
        ),
    ]