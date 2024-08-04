from bongapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    path("",views.index,name="home"),
    path("login",views.loginuser,name='loginuser'),
    path("logout",views.logoutuser,name='logoutuser'),
    path("signin",views.handlesignin,name='handlesignin'),
    path("prof",views.prof,name='prof'),
    path("booking",views.booking,name='booking'),
    path("menu",views.menu,name='menu'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path("cart",views.cart,name='cart'),
    path("create-checkout-session",views.createcheckoutsession,name='/create-checkout-session'),
    path('success/', views.payment_success, name='payment_success'),
    path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    path('ordertracker',views.ordertracker,name="ordertracker"),
    path('list-orders/', views.list_orders, name='list_orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# store image url
