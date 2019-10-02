from django.contrib import admin

# Register your models here.

from computerapps.models import Product, Category, Manufacturer, UserProfile, \
    DeliveryAddress, Order
from django.contrib.auth.models import User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'nickname', 'mobile_phone', 'description', 'icon']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ManufactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'price', 'category', 'manufacturer',
                    'sold', 'category', 'description']


class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'contact_person', 'contact_mobile_phone',
                    'delivery_address']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'product', 'price', 'quantity',
                    'address', 'remark']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufactureAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(DeliveryAddress, DeliveryAddressAdmin)
admin.site.register(Order, OrderAdmin)
