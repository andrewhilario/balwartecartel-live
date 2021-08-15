from .models import *
from .forms import  ChangePassword, CreateUserForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UserModel
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .helpers import send_forgot_password_mail
from django.http import JsonResponse
import json
import uuid
import datetime 

@login_required(login_url='/login')
def index(request): 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'cartitems': cartItems}
    return render(request, 'index.html', context)

@login_required(login_url='/login')
def products(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']



    products = Products.objects.all()
    context = {'products': products, 'cartitems': cartItems, 'shipping': False}
    return render(request, 'users/products.html', context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def login_form(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.success(request, 'Both Username and Password are required!')
                return redirect('/login')
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, 'User not Found!')
                return redirect('/login')

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.success(request, 'Wrong Username or Password')
                return redirect('/login')

            login(request, user)
            return redirect('/')
    except Exception as e:
        print(e)
    context = {}
    return render(request, 'users/login.html', context)

    # if request.user.is_authenticated:
    #     return redirect('/')
    # else:
    #     if request.method == 'POST':
    #         username = request.POST.get('username')
    #         password = request.POST.get('password')

    #         user = authenticate(request, username=username, password=password)

    #         if user is not None:
    #             login(request, user)
    #             return redirect('/')
    #         else:
    #             messages.info(request, 'Username or Password is incorrect')

def register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
        
        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is Taken')
                return redirect('/register')
            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is Taken')
                return redirect('/register')
            
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            profile_obj = Profile.objects.create(user=user_obj)
            profile_obj.save()
            customer = Customer.objects.create(user=user_obj)
            customer.save()
            messages.success(request, 'Account Created for ' + username)
            return redirect('/login')

        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    return render(request, 'users/register.html')
    

    # if request.user.is_authenticated:
    #     return redirect('/')
    # else:
    #     form = CreateUserForm()
    #     if request.method == 'POST':
    #         form = CreateUserForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             username = form.cleaned_data.get('username')
    #             messages.success(request, 'Account was created for ' + username)

    #             return redirect('/login')
    #     context = {'form': form}
    #     return render(request, 'users/register.html', context)
def change_password(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id': profile_obj.user.id}
            
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No User Id Found')
                return redirect(f'/change-password/{token}')

            if new_password != confirm_password:
                messages.success(request, 'Password does not match')
                return redirect(f'/change-password/{token}')

            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Your password has been changed')
            return redirect('/login')

        
    except Exception as e:
        print(e)
    return render(request, 'users/change_password.html', context)
def forgot_password(request): 
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'User not found')
                return redirect('forgot-password')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forgot_password_mail(user_obj.email , token)
            messages.success(request, 'Email Sent!')
            return redirect('/forgot-password')

    except Exception as e:
            print(e)
            
    return render(request, 'users/forgot_password.html')





    
        # if request.method == 'POST':
        #     form = ChangePassword(request.user, request.POST)
        #     if form.is_valid():
        #         user = form.save()
        #         update_session_auth_hash(request, user)  # Important!
        #         messages.success(request, 'Your password was successfully updated!')
        #         return redirect('password_reset_confirm')
        #     else:
        #         messages.error(request, 'Please correct the error below.')
        # else:
        #     form = ChangePassword(request.user)
        # return render(request, 'users/change_password.html', {
        #     'form': form
        # })


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete =False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0 , 'shipping': False}
    context = {'items': items, 'order': order , 'shipping': False}
    return render(request, 'users/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete =False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False }
    context = {'items': items, 'order': order}
    return render(request, 'users/checkout.html', context)
    
def updateItem(request):
    data =  json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('Product ID: ', productId)

    customer = request.user.customer
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete =False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added ', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete =False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['province'],
                zipcode=data['shipping']['zipcode'],
            )
         
    else:
        print('User is not logged in')



    return JsonResponse('Payment submitted...', safe=False)
    