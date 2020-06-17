from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    display = ('name', 'price')


admin.site.register(Product, ProductAdmin)
