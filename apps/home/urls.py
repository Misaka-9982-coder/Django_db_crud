

from django.contrib import admin
from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    
    
    path('bags_table', views.show_bags, name="show_bags"),
    path('designers_table', views.show_designers, name="show_designers"),
    path('customers_table', views.show_customers, name="show_customers"),
    path('rentals_table', views.show_rentals, name="show_rentals"),
    
    
    path('customer_register', views.customer_register, name="customer_register"),
    path('reset_pass', views.reset_pass, name="reset_pass"),
    
    
    path('bag_views', views.bag_views, name="bags_views"),
    path('best_customer', views.best_customer, name="best_customer"),
    path('customers_amount', views.customers_amount, name="customers_amount"),
    path('add_bag', views.add_bag, name="add_bag"),
    path('rent_bag', views.rent_bag, name="rent_bag"),
    path('mybag', views.mybag, name="mybag"),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
