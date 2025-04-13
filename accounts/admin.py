from django.contrib import admin
from .models import Restaurant, Dish, Order, OrderItem, Review, Cart


admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Cart)
