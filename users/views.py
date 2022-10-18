from operator import is_
from pkgutil import iter_modules
from django.shortcuts import render, redirect
from django.contrib import messages
from sympy import re
from users.models import Profile
from .forms import *
from marketplace.utils import context_objects
from marketplace.models import Customer, ProductOrder, UserShippingAddress
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from django.http import JsonResponse
from decimal import Decimal
# Create your views here.

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} succesfully created')
            user = form.save()

            Customer.objects.create(user=user, name=form.cleaned_data.get('username'), email=form.cleaned_data.get('email'))
            Profile.objects.create(user=user, phone_number=form.cleaned_data.get('phone'))
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form, 'title':'Registration'})

@login_required
def user_profile(request):
    order, products, cart_items = context_objects(request)
    ordered_items = ProductOrder.objects.filter(customer = request.user.customer, complete = True).order_by('-date_ordered')

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account details succesfully changed')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
            
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'order': order,
        'products': products,
        'cart_items': cart_items,
        'ordered_items': ordered_items,
        'title': f'{request.user.first_name} {request.user.last_name}'
    }

    return render(request, 'users/profile.html', context)

def check_if_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(check_if_admin)
def logistics_dashboard(request):
    order, products, cart_items = context_objects(request)
    product_order = UserShippingAddress.objects.all().order_by('-order')

    filter = UserShippingAddressFilter(request.GET, queryset=product_order)
    product_order = filter.qs
 
    context = {
        'product_order':product_order,
        'cart_items': cart_items,
        'filter': filter,
        'title': 'Logistics Dashboard'
    }
    return render(request, 'users/logistics_dashboard.html', context)

@login_required
@user_passes_test(check_if_admin)
def accounting_dashboard(request):
    order, products, cart_items = context_objects(request)
    product_order = UserShippingAddress.objects.all().order_by('-order')

    filter = UserShippingAddressFilter(request.GET, queryset=product_order)
    product_order = filter.qs

    def balance_per_customer(product_order):
        sales = {}

        for items in product_order:
            name = items.customer.name
            x = sum([items.order.total_order_cost for items in product_order if items.customer.name == name])
            y = sum([items.order.amount_paid for items in product_order if items.customer.name == name])
            data = (name, x-y)
            sales[data[0]] = data[1]

        sorted_sales = sorted(sales.items(), key=lambda x: x[1], reverse=True)
        sorted_dict = {}
        for items in sorted_sales:
            sorted_dict[items[0]] = items[1]

        return sorted_dict

    metrics = {
        'balance_per_customer': balance_per_customer(product_order)
    }
 
    context = {
        'product_order':product_order,
        'cart_items': cart_items,
        'filter': filter,
        'metrics':metrics,
        'title': 'Accounting Dashboard'
    }
    return render(request, 'users/accounting_dashboard.html', context)

@login_required
@user_passes_test(check_if_admin)
def sales_dashboard(request):
    order, products, cart_items = context_objects(request)
    product_order = UserShippingAddress.objects.all().order_by('-order')
    filter = UserShippingAddressFilter(request.GET, queryset=product_order)
    product_order = filter.qs

    total_gross_sales = sum([items.order.total_order_cost for items in product_order])
    total_pending_sales = sum([items.order.total_order_cost for items in product_order if items.order.payment_status == 'PENDING'])
    total_paid_sales = sum([items.order.total_order_cost for items in product_order if items.order.payment_status == 'PAID'])
    total_cancelled_sales = sum([items.order.total_order_cost for items in product_order if items.order.payment_status == 'CANCELLED'])

    total_orders = len(product_order)
    total_pending_delivery_orders = len([items for items in product_order if items.order.delivery_status == 'PENDING'])
    total_for_delivery_orders = len([items for items in product_order if items.order.delivery_status == 'FOR DELIVERY'])
    total_delivered_orders = len([items for items in product_order if items.order.delivery_status == 'DELIVERED'])


    def get_items_data(product_order):
        initial_list = [items.order.ordered_items for items in product_order]
        cleaned_list = [items.strip('{}') for items in initial_list]
        cleaned_list = [items.split(',') for items in cleaned_list]

        items_data = {}
        
        for items in cleaned_list:
            for x in items:
                if x == '':
                    pass
                else:
                    y = x.split(':')
                    if y[0].lstrip() in items_data:
                        items_data[y[0].lstrip()] = items_data[y[0].lstrip()] + int(y[1].lstrip())
                    else:
                        items_data[y[0].lstrip()] = int(y[1].lstrip())

        sorted_data = sorted(items_data.items(), key=lambda x: x[1], reverse=True)

        sorted_items_data = {}
        for items in sorted_data:
            sorted_items_data[items[0]] = items[1]

        return sorted_items_data

    def sales_per_customer(product_order):
        sales = {}

        for items in product_order:
            name = items.customer.name
            order = sum([items.order.total_order_cost for items in product_order if items.customer.name == name])
            data = (name, order)
            sales[data[0]] = data[1]

        sorted_sales = sorted(sales.items(), key=lambda x: x[1], reverse=True)
        sorted_dict = {}
        for items in sorted_sales:
            sorted_dict[items[0]] = items[1]

        return sorted_dict

    metrics = {
        'total_gross_sales':total_gross_sales,
        'total_pending_sales':total_pending_sales,
        'total_paid_sales':total_paid_sales,
        'total_cancelled_sales':total_cancelled_sales,
        'total_orders':total_orders,
        'total_pending_delivery_orders':total_pending_delivery_orders,
        'total_for_delivery_orders':total_for_delivery_orders,
        'total_delivered_orders':total_delivered_orders,
        'items_data':get_items_data(product_order),
        'sales_per_customer':sales_per_customer(product_order)
    }

    # print(total_gross_sales, total_orders, total_pending_delivery_orders, total_for_delivery_orders, get_items_data(product_order),sales_per_customer(product_order))
    context = {
        'product_order':product_order,
        'cart_items': cart_items,
        'filter': filter,
        'metrics':metrics,
        'title': 'Sales Dashboard'
    }
    return render(request, 'users/sales_dashboard.html', context)    

def status_update(request):
    data = json.loads(request.body)
    name = data['name']
    action = data['action']
    value = data['choice_value']

    order= ProductOrder.objects.get(transaction_id = name)

    if action == 'delivery':
        order.delivery_status = value
    elif action == 'payment':
        order.payment_status = value

    order.save()

    return JsonResponse('Item was added', safe=False)


def payment_update(request):
    data = json.loads(request.body)
    id = data['name']
    value = data['choice_value']

    order = ProductOrder.objects.get(transaction_id = id)
    order.amount_paid = value
    
    order.save()

    return JsonResponse('Item was added', safe=False)


