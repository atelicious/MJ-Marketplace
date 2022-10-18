from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import context_objects
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from random import randrange
from decimal import Decimal

def home(request):

    order, products, cart_items = context_objects(request)

    products = Products.objects.all().order_by('name')
    context = {
        'products': products,
        'title': 'Marketplace',
        'cart_items':cart_items
    }
    return render(request, 'marketplace/home.html', context)

@login_required
def cart(request):

    order, products, cart_items = context_objects(request)

    context = {
        'products': products,
        'product_order': order,
        'cart_items':cart_items,
        'title' : 'Cart'
    }

    return render(request, 'marketplace/cart.html', context)

@login_required
def checkout(request):

    order, products, cart_items = context_objects(request)

    context = {
        'products': products,
        'product_order': order,
        'cart_items': cart_items,
        'title' : 'Checkout'
    }

    return render(request, 'marketplace/checkout.html', context)


def show_faqs(request):

    order, products, cart_items = context_objects(request)
    context = {
        'cart_items': cart_items,
        'title' : 'Frequently Asked Questions'
    }

    return render(request, 'marketplace/faqs.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Products.objects.get(id = product_id)
    order, created = ProductOrder.objects.get_or_create(customer = customer, complete = False)
    order_item, created = PurchaseOrder.objects.get_or_create(order = order, product = product)

    if action == 'add':
        order_item.product_qty = (order_item.product_qty + 1)
    elif action == 'minus':
        order_item.product_qty = (order_item.product_qty - 1)

    order_item.save()

    if order_item.product_qty <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)

def process_order(request):
    data = json.loads(request.body)
    print('data', request.body)
    transaction_id = f'{datetime.now().strftime("%m%d%Y")}-{randrange(10000, 99999)}'

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = ProductOrder.objects.get_or_create(customer = customer, complete = False)
        total = data['form']['total']
        order.transaction_id = transaction_id

        #add total order cost here and items

        order.complete = True
        order.total_order_cost = order.get_cart_total_cost
        order.total_order_items = order.get_cart_total_items
        order.ordered_items = order.get_cart_items 
        order.delivery_status = 'PENDING'
        order.payment_status = 'PENDING'
        order.save()

        UserShippingAddress.objects.create(
            customer = customer,
            order = order,
            home_street = data['shipping']['inputAddress'],
            municipality_city = data['shipping']['inputCity'],
            province = data['shipping']['inputProvince'],
            country = data['shipping']['inputCountry'],
            zip_code = data['shipping']['inputZip'],
        )

    return JsonResponse('Order submitted', safe=False)