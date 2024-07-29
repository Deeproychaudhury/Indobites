from django.shortcuts import render,redirect,HttpResponse
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from .forms import Profileform,Userupdate,Bookform
from .models import Profile,product,Booking
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth import get_user_model
from math import ceil
import json
from django.db.models import Count

# Create your views here.
def logoutuser(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

def loginuser(request):
   if request.method == "POST":
     username=request.POST.get('username')
     password=request.POST.get('password')
     user = authenticate(username=username, password=password)
     if user is not None:
    # A backend authenticated the credentials
        login(request,user)
        return redirect("/")
     else:
    # No backend authenticated the credentials
        return render(request,'login.html')
   return render(request,'login.html')
  

  
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
   if request.method == "POST":# 2 types of form  request get post
      email=request.POST.get('email')
      name=request.POST.get('name')
      title=request.POST.get('title')
      phone=request.POST.get('phone')
      password=request.POST.get('password')
      #check error
      
      #create the user
      myuser=User.objects.create_user(name,email,password)
 #     user.first_name = request.POST.get('first_name')
  #    user.last_name = request.POST.get('last_name')
      myuser.first_name=name
      myuser.last_name=title
      myuser.save()
      user = authenticate(username=name, password=password)
      if user is not None:
    # A backend authenticated the credentials
        login(request,user)
        return redirect("/")
      messages.success(request,'Profile made')
      return redirect("/")
   return render(request,'CreateAccount.html')

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