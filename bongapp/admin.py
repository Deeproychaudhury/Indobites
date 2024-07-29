from django.contrib import admin

# Register your models here.
from .models import Profile,product,Booking

admin.site.register(Profile)
admin.site.register(product)

admin.site.register(Booking)