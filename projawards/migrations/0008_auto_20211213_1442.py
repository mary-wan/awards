# Generated by Django 2.2.24 on 2021-12-13 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projawards', '0007_auto_20211213_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
