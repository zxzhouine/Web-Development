# Generated by Django 2.1.1 on 2018-10-02 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0012_auto_20181002_0805'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='bio',
            new_name='intro',
        ),
    ]
