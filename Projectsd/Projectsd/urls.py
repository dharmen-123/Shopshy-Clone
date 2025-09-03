"""
URL configuration for Projectsd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static
from appsd import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login/',views.login_user,name='login_user'),
    path('logout/',views.logout_user,name='logout_user'),
    path('register/',views.register_user,name='register_user'),
    path('user_/my_account/changepassword/',views.change_password_page,name='change_password_page'),
    path('user_/my_account/_changepassword/',views.changepassword_user,name='changepassword_user'),
    path('user_/viewcart/',views.cart_user,name='cart_user'),
    path('viewcart/',views.login_cart,name='login_cart'),
    path('user_/my_account/',views.my_account,name='my_account'),
    path('login_/shopsy_dash_#/@&UR_admin/',views.admin_panel,name='admin_panel'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('login_/shopsy_dash_#/@&UR_admin/add_product/',views.add_product_btn,name='add_product'),
    path('show_item-products/<str:ds>/U40R<int:pk>9YJR/LRUSI3-84?DIZ92/',views.show_item,name='show_item'),
    path('add_to_cart/<str:ds>/<int:pk>/UI37Lr',views.add_to_cart,name='add_to_cart'),
    path('customers/',views.customers,name='customers'),
    path('removeitem/<int:pk>/',views.remove_item,name='remove_item'),
    path('increase_quantity/<int:pk>/',views.increase_quantity,name='increase_quantity'),
    path('decrease_quantity/<int:pk>/',views.decrease_quantity,name='decrease_quantity'),
    path('submit_product/',views.submit_product,name='submit_product'),
    path('admin_/allproduct-list/',views.admin_all_product,name='admin_all_product'),
    path('user_/delivery-address/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('paymenthandle/',views.paymenthandle,name='paymenthandle'),
    path('user_/delivery-address/',views.user_address,name='user_address'),
    path('user_/deliveryaddres/',views.selectaddress,name='selectaddress'),
    path('products/<str:name>/',views.categoryproducts,name='categoryproducts'),
    path('searchdata/',views.searchvalue,name='searchvalue'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
