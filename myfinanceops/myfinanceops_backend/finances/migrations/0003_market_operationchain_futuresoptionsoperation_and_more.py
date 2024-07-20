# Generated by Django 5.0.6 on 2024-07-13 18:04

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0002_remove_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='OperationChain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FuturesOptionsOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('trader', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_futures_options_operations', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_futures_options_operations', to=settings.AUTH_USER_MODEL)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.market')),
                ('operation_chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='futures_options_operation_chain', to='finances.operationchain')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FuturesOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('trader', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_futures_operations', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_futures_operations', to=settings.AUTH_USER_MODEL)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.market')),
                ('operation_chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='futures_operation_chain', to='finances.operationchain')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('trader', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_stock_operations', to=settings.AUTH_USER_MODEL)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.market')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_stock_operations', to=settings.AUTH_USER_MODEL)),
                ('operation_chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_operation_chain', to='finances.operationchain')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]