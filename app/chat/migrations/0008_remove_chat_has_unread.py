# Generated by Django 4.1 on 2022-10-19 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_message_options_message_is_edit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='has_unread',
        ),
    ]