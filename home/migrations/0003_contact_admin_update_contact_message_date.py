# Generated by Django 4.0.5 on 2022-06-13 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_contact_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='admin_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='message_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
