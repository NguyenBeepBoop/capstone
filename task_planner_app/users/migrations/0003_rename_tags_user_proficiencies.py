# Generated by Django 3.2.13 on 2022-07-12 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='tags',
            new_name='proficiencies',
        ),
    ]
