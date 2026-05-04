from django.contrib import admin

from .models import (
    OrderItem,
    Order
)

admin.site.register(OrderItem)
admin.site.register(Order)


# Register your models here.
