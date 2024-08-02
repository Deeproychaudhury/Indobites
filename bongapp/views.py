from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseBadRequest
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from .forms import Profileform,Userupdate,Bookform
from .models import Profile,Product,Booking,OrderModel
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth import get_user_model
from math import ceil
from django.views import View
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
def logoutuser(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')



def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            if is_ajax:
                return JsonResponse({"success": True}, status=200)
            else:
                return redirect("/")
        else:
            error_message = "Invalid username or password."
            if is_ajax:
                return JsonResponse({"error": error_message}, status=400)
            else:
                messages.error(request, error_message)
                return render(request, 'login.html')
    return render(request, 'login.html')


  
def index(request):
    if request.user.is_anonymous:
        value="customer"
        sign=False
    else:
       value=request.user.username
       sign=True
    context={
        'value':value,
        'sign':sign
             }
    return render(request,'index.html',context)


def handlesignin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        title = request.POST.get('title')  # Assuming 'title' is meant to be last name or similar
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Check if all required fields are provided
        if not name or not email or not password or not title:
            messages.error(request, "All fields are required.")
            return redirect("/signin")

        # Create the user
        try:
            myuser = User.objects.create_user(username=name, email=email, password=password)
            myuser.first_name = name
            myuser.last_name = title  # Assign the title or last name
            myuser.save()

            # Authenticate and log the user in
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Profile created successfully.')
                return redirect("/")
            else:
                messages.error(request, "Authentication failed. Please try logging in.")
                return redirect("/login")

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("/signin")

    return render(request, 'CreateAccount.html')

def prof(request):
    if request.user.is_anonymous:
       return redirect("/login")
    
    if request.method == 'POST':
      uform=Userupdate(request.POST,instance=request.user)
      pform=Profileform(request.POST,
                        request.FILES,
                        instance=request.user.profile)
      if uform.is_valid() and pform.is_valid():
         uform.save()
         pform.save()
         messages.success(request, 'Profile update done')
         return redirect("prof")

    else:
      uform=Userupdate(instance=request.user)
      pform=Profileform(instance=request.user.profile)
    jei=request.user.username
    all_users=Booking.objects.filter(name=jei)

    content={'uform':uform,
             'pform':pform,
             'all_users':all_users
             }
    return render(request,'ProfileCustomer.html',content)

def menu(request):
   if request.method == 'POST':
      filter_query=request.POST.get('select')
      search_query=request.POST.get('searchMenu')
   else:
      filter_query='Biriyani'
      search_query='###'
   if search_query=="":
      search_query="###"
   prodobject=Product.objects.all()
   cat1= Product.objects.filter(category=filter_query)
   cati2=prodobject.filter( product_name__icontains=search_query)|prodobject.filter(category__icontains=search_query)|prodobject.filter(price__startswith=search_query)
   cat2=cati2.values()
   if request.user.is_anonymous:
        value="customer"
        sign=False
   else:
       value=request.user.username
       sign=True
    
   context={
         'objects':prodobject,
         'value':value,
         'sign':sign,
         'cat1':cat1,
         'deli':filter_query,
         'cat2':cat2

    }
   return render(request,'menu.html',context)

#class Cart(View):
@login_required
def add_to_cart(request):
    if request.method=='POST':
     product=request.POST.get('obj_id')
     quantity=request.POST.get('quantity')
     if not product or not quantity:
         messages.error(request,"Invalid input in add to cart")
    phone= request.user.profile.phone 
    try:
            product = Product.objects.get(id=product)
    except Product.DoesNotExist:
            return HttpResponseBadRequest("Product not found")
    
    order=OrderModel(
        product=product,
        phone=phone,
        customer=request.user,
        quantity=quantity,
        price=product.price * int(quantity)
        
     )
    order.save()
    messages.success(request,"Item added. Proceed to checkout or add browse other items")
    return redirect('menu')

@login_required
def cart(request):
      orders=OrderModel.objects.filter(customer=request.user)
      count=orders.count() #count number of orders
      sum=0
      for ord in orders:
          sum+=ord.price
      if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

        order = get_object_or_404(OrderModel, id=order_id, customer=request.user)

        if action == 'update':
            quantity = request.POST.get('quantity')
            if quantity is not None:
                try:
                    new_quantity = int(quantity)
                    if new_quantity > 0:
                        order.quantity = new_quantity
                        order.price = order.product.price * new_quantity
                        order.save()
                    else:
                        order.delete()
                        messages.success(request, "Item removed from cart")
                except ValueError:
                    messages.error(request, "Invalid quantity")
        elif action == 'delete':
            order.delete()
            messages.success(request, "Item removed from cart")

        return redirect('cart')

      return render(request, 'cart.html', {'orders': orders, 'count': count, 'value': request.user.username, 'sum': sum})

def booking(request):
     if request.user.is_anonymous:
       return redirect("/login")
     if request.method == 'POST':
        email=request.POST.get('email')
        dateofuser=request.POST.get('date')
    #    dateof = datetime.strptime(dateo,'%m-%d-%y')
     #   dateofuser= datetime.strftime(dateof,'%Y-%m-%d')
        descr=request.POST.get('descr')
        seats=request.POST.get('select')
        phone=request.POST.get('phone')
        name2=request.POST.get('name')
      
        if Booking.objects.filter(day=dateofuser).count() < 1:
           book=Booking(email=email,phone=phone,name=name2,seats=seats,description=descr,day=dateofuser)
           book.save()
           messages.success(request, "Appointment Saved!")
           return redirect("/prof")
     context={'seats': ["2", "4","10","20", "30+(buffet)"
                  ],}
     return render(request,'profile.html',context)