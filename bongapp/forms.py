from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Booking
from django.forms import TextInput,EmailInput,ImageField

class Bookform(forms.ModelForm):
   date=forms.DateField()

   class Meta:
      model=Booking
      fields=['date']

class Userupdate(forms.ModelForm):
   email=forms.EmailField()

   class Meta:
      model =User
      fields=['username','email']
      widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                
                'placeholder': 'Name'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                
                'placeholder': 'Email'
                })
        }

class Profileform(forms.ModelForm):
   phone=forms.IntegerField()
   review=forms.CharField()

   class Meta:
      model=Profile
      fields= ['image','phone','review']
      widgets = {
            'review': TextInput(attrs={
                'class': "form-control",
                'style': 'style="color :#A82C48"',
                'placeholder': 'Name'
                }),
            'phone': EmailInput(attrs={
                'class': "form-control", 
                'placeholder': 'Email'
                })
        }