# Generated by Django 5.0.6 on 2024-08-02 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0019_alter_commissions_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockoperation',
            name='shares_amount',
            field=models.IntegerField(),
        ),
    ]