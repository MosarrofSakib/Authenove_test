from django.urls import path
from . import views


urlpatterns = [
    path('', views.latestProductsView, name='home' ),
    path('register/', views.registerPage, name='register' ),
    path('login/', views.loginPage, name='login' ),
    path('logout/', views.logoutUser, name='logout' ),
    path('profile/', views.userProfile, name='profile'),
    path('products/', views.productsView, name= 'products'),
    path('single_product/<str:pk>', views.singleProductsView, name= 'single_product'),
    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('dashboard/orders', views.allOrders, name= 'orders'),
    path('dashboard/customers', views.allCustomers, name= 'customers'),
    path('dashboard/orders/order_details/<str:pk>', views.updateOrder, name= 'order_details'),
    path('dashboard/customers/customer_details/<str:pk>', views.customerDetails, name= 'customer_details'),

]