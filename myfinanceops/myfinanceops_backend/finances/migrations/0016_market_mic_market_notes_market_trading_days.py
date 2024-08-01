# Generated by Django 5.0.6 on 2024-07-31 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0015_operationchain_chain_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='mic',
            field=models.CharField(default=1, max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='market',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='market',
            name='trading_days',
            field=models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], default=1, max_length=255),
            preserve_default=False,
        ),
    ]