# Generated by Django 4.0.5 on 2022-06-28 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_shopcart_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcart',
            old_name='created',
            new_name='created_at',
        ),
    ]
