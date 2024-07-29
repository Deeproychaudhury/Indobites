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
    path("cart",views.cart,name='cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# store image url
