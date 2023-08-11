from django.contrib import admin

from .models import *

class OrderFileInline (admin.StackedInline):
    model = OrderFile
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderFileInline]

class ServiceTabInline (admin.StackedInline):
    model = ServiceTab
    extra = 0
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    inlines = [ServiceTabInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(Direction)
admin.site.register(Country)
admin.site.register(Service, ServiceAdmin)
admin.site.register(PayStatus)
admin.site.register(OrderStatus)
admin.site.register(Banner)
admin.site.register(CallbackForm)



