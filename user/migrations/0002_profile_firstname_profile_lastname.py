# Generated by Django 5.0.2 on 2024-03-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='firstName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='lastName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]