# Generated by Django 3.1.2 on 2020-10-09 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_user_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='title',
            new_name='name',
        ),
    ]