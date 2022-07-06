from django.contrib import admin
from .models import Copun, Order, OrderItem
from django.contrib.admin import DateFieldListFilter
#
# Register your models here.
admin.site.register(Copun)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'copun', 'total', 'address', 'get_phone')
    list_filter = ('is_processed', 'cod', ('timestamp', DateFieldListFilter))

    inlines = [OrderItemInline]

    def get_phone(self, obj):
        return obj.address.phone

    get_phone.short_description = 'Phone'
    get_phone.admin_order_field = 'address__phone'

admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)