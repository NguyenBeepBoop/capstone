# Generated by Django 3.2.13 on 2022-07-25 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_notification_friend_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='friend_request',
        ),
    ]
