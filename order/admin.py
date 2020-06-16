from django.contrib import admin
from .models import Order
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    display = ('user',)


admin.site.register(Order, OrderAdmin)
