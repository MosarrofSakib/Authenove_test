import json
import datetime
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group

from . import models
from .form import OrderForm,CreateUserForm
from .filter import OrderFilter,ProductFilter
from .utils import cookieCart, cartData, guestOrder
from .decorators import unauthenticated_user,admin_only
# Create your views here.


#user authentication starts here

@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
    context = {'form':form}
    return render(request, 'product/register.html', context)

@unauthenticated_user
def loginPage(request):
	
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, template_name='product/login.html', context= context) 

def logoutUser(request):
	logout(request)
	return redirect('login')
#user authentication ends here

#user profile
@login_required(login_url='login')
def userProfile(request):
    customer = request.user.customer
    orders = models.Order.objects.filter(customer=customer,complete=True).order_by("-date_created")
    #order_item = orders.orderItem_set.all()
    #print('order_item',order_item)
    
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    total_orders = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }
    return render(request, template_name='product/profile.html', context= context)


#showing products and cart
def latestProductsView(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = models.Product.objects.all().order_by("-date_created")[0:12]
    context = {
        'products': products,
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }

    return render(request, template_name='product/index.html', context= context)


def productsView(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = models.Product.objects.all()

    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs

    context = {
        'products': products,
        'product_filter': productFilter,
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }

    return render(request, template_name='product/products.html', context= context)


def singleProductsView(request, pk):
    data = cartData(request)
    id=pk
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    product = models.Product.objects.get(id=pk)
    
    """ single_item = []
    for item in items:
        if int(item['id']) == product.id:
            single_item = item
        else:
            single_item = [] """

    context = {
        'product': product,
        'cartItems': cartItems,
        'order': order,
        'items': items, 
    }
    return render(request, template_name='product/single_product.html', context= context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'product/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'product/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = models.Product.objects.get(id=productId)
	order, created = models.Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    order_status = "Pending"
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.status = order_status
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    
    models.ShippingAddress.objects.create(
        customer=customer,
        order=order,
        phone_no = data['shipping']['phone_no'],
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        )

    return JsonResponse('Your order completed', safe=False)
    

#admin panel views starts here
@login_required(login_url='login')
@admin_only
def dashboard(request):
    
    customers_latest = models.Customer.objects.all().order_by("-date_created")[0:10]
    orders_latest = models.Order.objects.filter(complete=True).order_by("-date_created")[0:10]
    total_orders = models.Order.objects.filter(complete=True).count()
    pending = models.Order.objects.filter(status='Pending').count()
    delivered = models.Order.objects.filter(status='Delivered').count()

    context ={
        'customers_latest': customers_latest,
        'orders_latest': orders_latest,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered,
    }
    return render(request, template_name='product/dashboard.html', context= context)

@login_required(login_url='login')
@admin_only
def customerDetails(request,pk):
    customer = models.Customer.objects.get(id=pk)
    orders = models.Order.objects.filter(customer=customer,complete=True).order_by("-date_created")

    total_orders = orders.count()

    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs

    context ={
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'filter': orderFilter,
    }
    return render(request, template_name='product/customer_details.html', context= context)


@login_required(login_url='login')
@admin_only
def allOrders(request):
    orders = models.Order.objects.filter(complete=True).order_by("-date_created")
    total_orders = models.Order.objects.all().count()
    pending = models.Order.objects.filter(status='Pending').count()
    delivered = models.Order.objects.filter(status='Delivered').count()

    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs

    context ={
        'orders': orders,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered,
        'filter': orderFilter,
        
    }
    return render(request, template_name='product/orders_all.html', context= context)

@login_required(login_url='login')
@admin_only
def allCustomers(request):
    customers = models.Customer.objects.all().order_by("-date_created")
    context ={
        'customers' : customers,
    }
    return render(request, template_name='product/customers_all.html', context= context)

@login_required(login_url='login')
@admin_only
def updateOrder(request, pk):
    order = models.Order.objects.get(id=pk)
    orderItem = order.orderitem_set.all()
    ship_address = models.ShippingAddress.objects.filter(order= order)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders')


    context =  {
        'form':form,
        'order': order,
        'orderItem':orderItem,
        'ship_address': ship_address,
        }
    return render(request, 'product/order_details.html', context)