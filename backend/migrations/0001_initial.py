# Generated by Django 5.0.2 on 2024-03-22 02:52

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_profile_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand_name', models.CharField(max_length=100)),
                ('generic_name', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=100)),
                ('dosage', models.CharField(choices=[('tablet', 'Tablet'), ('capsule', 'Capsule'), ('suspension', 'Suspension')], max_length=100)),
                ('strength', models.CharField(max_length=100)),
                ('packaging_size', models.CharField(choices=[('100mg', '100mg'), ('200mg', '200mg'), ('300mg', '300mg'), ('400mg', '400mg'), ('500mg', '500mg'), ('30 capsules', '30 capsules'), ('60 capsules', '60 capsules'), ('90 capsules', '90 capsules')], max_length=100)),
                ('expiration_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stock_quantity', models.IntegerField()),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('shipped', models.BooleanField(default=False)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_status', models.CharField(choices=[('pending', 'pending'), ('processing', 'processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=100)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.drug')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='backend.order')),
            ],
        ),
    ]