# Generated by Django 4.1 on 2022-08-12 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_userprofile_city_userprofile_country_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
