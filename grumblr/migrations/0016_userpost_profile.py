# Generated by Django 2.1.1 on 2018-10-04 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0015_remove_userprofile_empty'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='grumblr.UserProfile'),
        ),
    ]
