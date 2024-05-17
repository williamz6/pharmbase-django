from django.contrib import admin
from .models import Drug, Order, OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["drug", "quantity", "total_price", "get_customer_list", "status"]

    def get_customer_list(self, obj):
        return ", ".join(str(customer) for customer in obj.getCustomer)

    get_customer_list.short_description = "Customers"


class orderItemInline(admin.TabularInline):
    model = OrderItem.orders.through
    extras = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [orderItemInline]


class DrugAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "manufacturer",
        "created",
        "expiration_date",
        "stock_quantity",
    ]


admin.site.register(Drug, DrugAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
