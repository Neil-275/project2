# Generated by Django 4.1.1 on 2022-10-10 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auction_item_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_item',
            name='closed',
            field=models.IntegerField(default=0),
        ),
    ]