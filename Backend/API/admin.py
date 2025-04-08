
from .models import *
from django.contrib import admin

admin.site.register(Warehouse)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(WarehouseProducts)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderProducts)
admin.site.register(PurchaseOrderShipping)