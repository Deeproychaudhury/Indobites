from django.contrib import admin

# Register your models here.
from .models import Profile,Product,Booking,OrderModel

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(OrderModel)

admin.site.register(Booking)