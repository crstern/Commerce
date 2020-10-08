# Generated by Django 3.1.2 on 2020-10-07 15:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('image', models.FileField(upload_to='images')),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=64)),
                ('isSold', models.BooleanField(default=False)),
                ('pulbication_date', models.DateField(default=datetime.datetime(2020, 10, 7, 18, 21, 49, 755660))),
                ('deadline', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('auctuion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]