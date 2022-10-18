# Generated by Django 2.2.5 on 2022-10-14 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0009_auto_20221012_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='pending_balance',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='productorder',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]