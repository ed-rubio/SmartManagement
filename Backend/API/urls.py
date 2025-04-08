
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'search', ProductSearchViewSet, basename='Search (Products)')

urlpatterns = [
    path('warehouses/', WarehouseListCreateView.as_view(), name='Warehouse (List/Create)'),
    path('warehouses/<str:slug>/', WarehouseRetrieveUpdateDestroyView.as_view(), name='Warehouse (Detail/Update/Delete)'),

    path('suppliers/', SupplierListCreateView.as_view(), name='Supplier (List/Create)'),
    path('suppliers/<str:slug>/', SupplierRetrieveUpdateDestroyView.as_view(), name='Supplier (Detail/Update/Delete)'),

    path('products/', ProductListCreateView.as_view(), name='Product (List/Create)'),
    path('products/<str:sku>/', ProductRetrieveUpdateDestroyView.as_view(), name='Product (Detail/Update/Delete)'),

    path('warehouse-products/', WarehouseProductsListCreateView.as_view(), name='WarehouseProducts (List/Create)'),
    path('warehouse-products/<str:slug>/', WarehouseProductsRetrieveUpdateDestroyView.as_view(), name='WarehouseProducts (Detail/Update/Delete)'),

    path('purchase-orders/', PurchaseOrderListCreateView.as_view(), name='PurchaseOrder (List/Create)'),
    path('purchase-orders/<str:slug>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='PurchaseOrder (Detail/Update/Delete)'),

    path('purchase-orders-products/', PurchaseOrderProductsListCreateView.as_view(), name='PurchaseOrderProducts (List/Create)'),
    path('purchase-orders-products/<str:slug>/', PurchaseOrderProductsRetrieveUpdateDestroyView.as_view(), name='PurchaseOrderProducts (Detail/Update/Delete)'),

    path('purchase-orders-shipping/', PurchaseOrderShippingListCreateView.as_view(), name='PurchaseOrderShipping (List/Create)'),
    path('purchase-orders-shipping/<str:slug>/', PurchaseOrderShippingRetrieveUpdateDestroyView.as_view(), name='PurchaseOrderShipping (Detail/Update/Delete)'),

    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='Login (C-GPT)'),
]