# Generated by Django 4.2.6 on 2023-10-18 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_predictions_from_date_predictions_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predictions',
            options={'verbose_name_plural': 'Predictions'},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['last_update'], 'verbose_name_plural': 'Stocks'},
        ),
        migrations.AlterModelOptions(
            name='stockdata',
            options={'verbose_name_plural': 'Stocks Data'},
        ),
    ]
