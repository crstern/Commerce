# Generated by Django 3.1.2 on 2020-10-18 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auction_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='publication_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]