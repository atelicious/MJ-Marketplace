from distutils.command.upload import upload
from random import choices
from django.db import models
from django.contrib.auth.models import User
from sympy import Product
from decimal import Decimal
import json



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)

    def __str__(self) -> str:
        return self.name

class Products(models.Model):
    name = models.CharField(max_length = 200, null = True)
    category = models.CharField(max_length = 200, null = True)
    price = models.FloatField()
    description = models.CharField(max_length = 300, null = True)
    product_img = models.ImageField(null = True, blank = True, upload_to='products')

    def __str__(self) -> str:
        return self.name

    @property
    def image_url(self):
        try:
            url = self.product_img.url
        except:
            url = ''

        return url

class ProductOrder(models.Model): #order
    del_status = [
        ('PENDING', 'PENDING'),
        ('FOR DELIVERY', 'FOR DELIVERY'),
        ('DELIVERED', 'DELIVERED')
    ]

    pay_status = [
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('CANCELLED', 'CANCELLED')
    ]

    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True, blank = False)
    transaction_id = models.CharField(max_length = 100, null = True)
    total_order_cost = models.DecimalField(max_digits = 12, decimal_places=2, null = True)
    total_order_items = models.IntegerField(null = True, blank = False)
    ordered_items = models.TextField(null = True, blank = False)
    delivery_status = models.CharField(default = 'PENDING', blank = False, choices=del_status, max_length = 20)
    payment_status = models.CharField(default = 'PENDING', blank = False, choices=pay_status, max_length = 20)
    amount_paid= models.DecimalField(max_digits = 12, decimal_places=2, default=Decimal('0.00'))


    def __str__(self) -> str:
        return str(self.id)

    @property
    def get_cart_total_cost(self):
        all_items = self.purchaseorder_set.all()
        #list comprehension here
        total = sum([items.get_total_cost for items in all_items])
        return total

    @property
    def get_cart_total_items(self):
        all_items = self.purchaseorder_set.all()
        #list comprehension here
        total = sum([items.product_qty for items in all_items])
        return total

    @property
    def get_cart_items(self):
        all_items = self.purchaseorder_set.all()
        item_dict = {}
        for items in all_items:
            item_dict[items.product.name]=items.product_qty
        return item_dict

    @property
    def get_order_balance(self):
        return self.total_order_cost - self.amount_paid

class PurchaseOrder(models.Model): #orderitem
    product = models.ForeignKey(Products, on_delete = models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(ProductOrder, on_delete = models.SET_NULL, null = True, blank = True)
    product_qty = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)

    @property
    def get_total_cost(self):
        total = self.product.price * self.product_qty
        return total

class UserShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(ProductOrder, on_delete = models.SET_NULL, null = True, blank = True)
    home_street = models.CharField(max_length = 200, null = True)
    municipality_city = models.CharField(max_length = 200, null = True)
    province = models.CharField(max_length = 100, null = True)
    country = models.CharField(max_length = 50, null = True)
    zip_code = models.CharField(max_length = 20, null = True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.home_street

    @property
    def get_address(self):
        return f'{self.home_street} {self.municipality_city} {self.province} {self.country},{self.zip_code}'






