# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.

from apps.home.models import * 

admin.site.register(Bag)
admin.site.register(Designer)
admin.site.register(Customer)
admin.site.register(Rentals)
