
from .views import *
from django.urls import path

urlpatterns = [
    path('productos/', ProductListCreateView.as_view(), name='Product (List/Create)'),
    path('productos/<str:sku>/', ProductRetrieveUpdateDestroyView.as_view(), name='Product (Detail/Update/Delete)'),

    # ...
]