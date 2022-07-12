# from email import message
import uuid
import json
import requests

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View

from . forms import ContactForm
from . forms import * 
from . models import *
# from . forms import SignupForm, ProfileUpdate 
# from . models import Product, Profile

# Create your views here.
def index(request):
    latest = Product.objects.filter(latest=True)
    trending = Product.objects.filter(trending=True)

    context = {
        'vic':latest,
        'math':trending,
    }

    return render(request, 'index.html', context)   

def contact(request):
    form = ContactForm()#instatiate the contactform for a GET request
    if request.method == 'POST': #make a POST REQUEST
        form = ContactForm(request.POST)#instatiate the contactform for a POST request
        if form.is_valid():#Django will validate the form
            form.save()#if valid, save the data to the DB
            messages.success(request, 'I don receive your message,')
            return redirect('index')#return to index once the post action is carried out
                
    return render(request, 'index.html')
  #return HttpResponse('Jeff is singing')

def products(request):
    product = Product.objects.all()

    context = {
        'product':product,
    }
    return render(request, 'products.html',context)


def details(request, id):
    details = Product.objects.get(pk=id)
    context = {
        'detail':details,
    }
    return render(request, 'details.html',context)




# authentication
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        usernamee = request.POST['username']
        passwrodd = request.POST['password']
        user = authenticate(request,username= usernamee, password=passwrodd )
        if user is not None:
            login(request, user)
            messages.success(request, 'signin successful')
            return redirect('index')
        else:
            messages.warning(request, 'username/password incorrect. kindly suplly valid details')
            return redirect('signin')
    return render(request, 'signin.html')


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        state = request.POST['state']
        address = request.POST['address']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            newprofile = Profile(victor = newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.state = state
            newprofile.address = address
            newprofile.pix = pix
            newprofile.save()
            login(request, newuser)
            messages.success(request, 'Signup successful')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')
# authentication done

# profile
@login_required(login_url='signin') 
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)

    context = {
        'profile':profile,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin') 
def profile_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    update = ProfileUpdate(instance = request.user.profile)#instantiate the form for  get request along with the user's details
    if request.method == 'POST':
        update = ProfileUpdate(request.POST, request.Files, instance = request.user.profile)#ins
        if update.is_valid():
            update.save()
            messages.success(request, 'Profile update successful')
            return redirect('profile')  
        else:  
            messages.error(request, update.errors)
            return redirect('profile_update')
    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html', context)


# profile done


@login_required(login_url='signin')
def password(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form  = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password change successful.')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('password')

    context = {
        'form':form,
        'profile':profile,
    }
    return render(request, 'password.html', context)

#shopcart
def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        item_id = request.POST['product_id']
        item = Product.objects.get(pk=item_id)
        order_num = Profile.objects.get(user__username = request.user.username)
        cart_no = order_num.id


        cart = Shopcart.objects.filter(user__username = request.user.username, paid= False)
        if cart:
            basket = Shopcart.objects.filter(product = item.id, user__username = request.user.username).first()
            if basket:
                basket.quantity += quant
                basket.amount = basket.price * quant
                basket.save()
                return redirect('products')
            else:
                newitem = Shopcart()
                newitem.user = request.user
                newitem.product = item
                newitem.quantity = quant
                newitem.price = item.price 
                newitem.amount = item.price * quant
                newitem.order_no = cart_no
                newitem.paid = False
                newitem.save()
                messages.success(request, 'Item added to Shopcart.')
                return redirect('products')
        else:
            newcart = Shopcart()
            newcart.user = request.user
            newcart.product = item
            newcart.quantity = quant
            newcart.price = item.price 
            newcart.amount = item.price * quant
            newcart.order_no = cart_no
            newcart.paid = False
            newcart.save()
            messages.success(request, 'Item added to Shopcart.')
            return redirect('products')

    return redirect('products')

@login_required(login_url='signin')
def displaycart(request):
    trolley = Shopcart.objects.filter(user__username = request.user.username, paid = False)
    profile = Profile.objects.get(user__username = request.user.username)

    subtotal = 0
    vat = 0
    total = 0

    for cart in trolley:
        subtotal = cart.price * cart.quantity

    vat = 0.075 * subtotal
    total = vat + subtotal

    context = {
        'trolley':trolley,
        'profile':profile,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }

    return render(request, 'displaycart.html', context)


def deleteitem(request):
    item_id = request.POST['item_id']
    item_delete = Shopcart.objects.get(pk=item_id)
    item_delete.delete()
    messages.success(request, 'item deleted successfully.')
    return redirect('displaycart')

def increase(request):
    if request.method == 'POST':
        the_item = request.POST['itemid']
        the_quant = int(request.POST['quant'])
        modify = Shopcart.objects.get(pk=the_item)
        modify.quantity = the_quant
        modify.amount =  modify.quantity * modify.price
        modify.save()
    return redirect('displaycart')
# shopcart done

# checkout using class based view and axios get request
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        summary = Shopcart.objects.filter(user__username = request.user.username, paid=False)

        
        subtotal = 0
        vat = 0
        total = 0

        for cart in summary:
            subtotal = cart.price * cart.quantity

        vat = 0.075 * subtotal
        total = vat + subtotal
        context = {
            'summary':summary,
            'total':total,
        }
        return render(request, 'checkout.html', context)
# checkout using class based view and axios get request done


@login_required(login_url='signin')
def pay(request):
    # integrating to paystack
    api_key = 'sk_test_f402fd47bcd811ea5aeaa5fb1fd4db18da58a5e8'
    curl = 'https://api.paystack.co/transaction/initialize '
    cburl = 'http://44.208.32.215/callback'
    # cburl = 'http://127.0.0.1:8000/callback'
    user = User.objects.get(username = request.user.username)
    email = user.email
    total = float(request.POST['total']) * 100
    cart_no = user.profile.id
    transac_code = str(uuid.uuid4())

    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'reference':transac_code, 'amount':int(total),'email':email, 'order_number':cart_no, 'callback_url':cburl, 'currency':'NGN'}
    try:
        r = requests.post(curl, headers=headers, json=data) 
    except Exception:
        messages.error(request, 'Network busy, refresh and try again')
    else:
        transback = json.loads(r.text)
        rdurl = transback['data']['authorization_url']
        return redirect(rdurl)
    return redirect('displaycart')

def callback(request):
    Profile = Profile.objects.get(user__username = request.user.username)
    cart =Shopcart.objects.filter(user__username = request.user.username, paid=False)

    for pro in cart:
        pro.paid = True
        pro.save()

        stock = Product.objects.get(pk=pro.item.product.id)
        stock.max_quantity -=pro.quantity
        stock.save()
    context = {
        'profile':profile,
    }
    return render(request, 'callback.html', context)
