
from django.contrib import admin

# Register your models here.

from apps.home.models import * 


# 后台注册 Models 类
admin.site.register(Bag)
admin.site.register(Designer)
admin.site.register(Customer)
admin.site.register(Rentals)
