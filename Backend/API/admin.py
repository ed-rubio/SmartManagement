
from .models import *
from django.contrib import admin

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(SupplierProducts)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)