# Generated by Django 4.0.5 on 2022-07-07 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_rename_victor_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(default='a', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(default='a', max_length=200),
        ),
    ]