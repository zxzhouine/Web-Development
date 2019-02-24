# Generated by Django 2.1.1 on 2018-10-04 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0017_userprofile_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='follow',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
    ]