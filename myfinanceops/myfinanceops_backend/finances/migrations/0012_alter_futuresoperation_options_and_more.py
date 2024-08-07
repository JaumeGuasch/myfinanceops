# Generated by Django 5.0.6 on 2024-07-28 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0011_futuresoperation_price_per_contract_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='futuresoperation',
            options={'verbose_name': 'Futures operation'},
        ),
        migrations.AlterModelOptions(
            name='futuresoptionsoperation',
            options={'verbose_name': 'Options operation'},
        ),
        migrations.AlterModelOptions(
            name='stockoperation',
            options={'verbose_name': 'Stocks operation'},
        ),
        migrations.AddField(
            model_name='futuresoperation',
            name='transaction_type',
            field=models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='BUY', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='futuresoptionsoperation',
            name='transaction_type',
            field=models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='BUY', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockoperation',
            name='transaction_type',
            field=models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='BUY', max_length=4),
            preserve_default=False,
        ),
    ]
