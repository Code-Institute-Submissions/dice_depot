# Generated by Django 3.0.8 on 2020-11-27 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20201127_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user_profile',
            new_name='user_profiles',
        ),
    ]
