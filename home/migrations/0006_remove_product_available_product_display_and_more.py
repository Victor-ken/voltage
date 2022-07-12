# Generated by Django 4.0.5 on 2022-06-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available',
        ),
        migrations.AddField(
            model_name='product',
            name='display',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='latest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='trending',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_quantity',
            field=models.IntegerField(default=False),
        ),
    ]