from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
# Create your views here.
def index(request):

    return render(request, 'index.html')

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context={'products':products, 'cartItems':cartItems}
    return render(request, 'store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = request.body.decode('utf-8')
    received_json_data = json.loads(data)
    productId = received_json_data['productId']
    action = received_json_data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse("Item was added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    # data = json.loads(request.body)
    data = request.body.decode('utf-8')
    received_json_data = json.loads(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)

    else:

        customer, order = guestOrder(request, received_json_data)

    total = float(received_json_data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping ==True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = received_json_data['shipping']['address'],
            city = received_json_data['shipping']['city'],
            state = received_json_data['shipping']['state'],
            zipcode = received_json_data['shipping']['zipcode']
        )

    return JsonResponse('Payment complete!', safe=False)
