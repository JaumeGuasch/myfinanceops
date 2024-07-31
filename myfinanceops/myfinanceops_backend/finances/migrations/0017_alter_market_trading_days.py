# Generated by Django 5.0.6 on 2024-07-31 03:42

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0016_market_mic_market_notes_market_trading_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='trading_days',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=255, null=True),
        ),
    ]
