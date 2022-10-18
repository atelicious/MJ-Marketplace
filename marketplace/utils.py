from .models import *

def context_objects(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = ProductOrder.objects.get_or_create(customer = customer, complete = False)
        products = order.purchaseorder_set.all()
        cart_items = order.get_cart_total_items
        return order, products, cart_items

    else:
        products = []
        order = {'get_cart_total_cost':0, 'get_cart_total_items': 0}
        cart_items = order['get_cart_total_items']
        return order, products, cart_items