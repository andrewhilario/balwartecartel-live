# Generated by Django 3.1.7 on 2021-07-05 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210705_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customer',
            new_name='user',
        ),
    ]