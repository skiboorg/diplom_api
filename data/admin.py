from django.contrib import admin

from .models import *

class OrderFileInline (admin.StackedInline):
    model = OrderFile
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderFileInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(PayStatus)
admin.site.register(OrderStatus)



