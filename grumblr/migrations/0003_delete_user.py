# Generated by Django 2.1.1 on 2018-09-20 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]