# Generated by Django 5.0.6 on 2024-07-21 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0006_futuresoperation_type_futuresoptionsoperation_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='futuresoperation',
            name='type',
            field=models.CharField(choices=[('Stock', 'Stock'), ('Futures', 'Futures'), ('Options', 'Options')], editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='futuresoptionsoperation',
            name='type',
            field=models.CharField(choices=[('Stock', 'Stock'), ('Futures', 'Futures'), ('Options', 'Options')], editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='stockoperation',
            name='type',
            field=models.CharField(choices=[('Stock', 'Stock'), ('Futures', 'Futures'), ('Options', 'Options')], editable=False, max_length=50),
        ),
    ]
