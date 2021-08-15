from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = "Balwarte Cartel Admin"
admin.site.site_title = "Balwarte Cartel Admin Area"

admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)