# Generated by Django 3.1.1 on 2021-05-02 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0006_auto_20210502_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightsdata',
            name='within_price_range',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
