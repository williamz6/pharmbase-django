from django.contrib import admin
from .models import Drug, Order, OrderItem



class orderItemInline(admin.TabularInline):
    model = OrderItem
    extras = 1


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
