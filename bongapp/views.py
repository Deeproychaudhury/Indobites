from django.shortcuts import render,redirect,HttpResponse
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from .forms import Profileform,Userupdate,Bookform
from .models import Profile,Product,Booking
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth import get_user_model
from math import ceil
import json
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
   prodobject=product.objects.all()
   cat1= product.objects.filter(category=filter_query)
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

def cart(request):
   return render(request,'Cart.html')

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