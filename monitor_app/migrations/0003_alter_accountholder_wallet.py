# Generated by Django 5.0 on 2023-12-12 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor_app', '0002_alter_accountholder_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountholder',
            name='wallet',
            field=models.IntegerField(default=0),
        ),
    ]
