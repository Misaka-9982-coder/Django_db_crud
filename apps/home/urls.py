

from django.contrib import admin
from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('bags_table', views.show_bags, name="show_bag"),
    path('designers_table', views.show_designers, name="show_designers"),
    path('customers_table', views.show_customers, name="show_customers"),
    path('rentals_table', views.show_rentals, name="show_rentals"),
    path('customer_register', views.customer_register, name="customer_register"),
    
    # re_path('stu/add/$', views.add_stu),
    # re_path('stu/(\d+)/delete', views.delete_stu),
    # re_path('stu/(\d+)/change', views.change_stu),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
