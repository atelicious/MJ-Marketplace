# Generated by Django 2.2.5 on 2022-10-05 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_products_product_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usershippingaddress',
            name='brgy',
        ),
    ]
