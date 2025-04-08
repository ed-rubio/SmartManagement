
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from rest_framework import generics, viewsets, filters, status


''' VISTAS: Almacenes. '''
class WarehouseListCreateView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WarehouseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    lookup_field = 'slug'


''' VISTAS: Proveedores. '''
class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = 'slug'


''' VISTAS: Productos. '''
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'sku'


''' VISTAS: Productos en almacén. '''
class WarehouseProductsListCreateView(generics.ListCreateAPIView):
    queryset = WarehouseProducts.objects.all()
    serializer_class = WarehouseProductsSerializer

class WarehouseProductsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WarehouseProducts.objects.all()
    serializer_class = WarehouseProductsSerializer
    lookup_field = 'slug'


''' VISTAS: Órdenes de compra. '''
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'slug'


''' VISTAS: Productos (OC-R). '''
class PurchaseOrderProductsListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrderProducts.objects.all()
    serializer_class = PurchaseOrderProductsSerializer

class PurchaseOrderProductsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrderProducts.objects.all()
    serializer_class = PurchaseOrderProductsSerializer
    lookup_field = 'slug'


''' VISTAS: Costos de envío (OC-R). '''
class PurchaseOrderShippingListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrderShipping.objects.all()
    serializer_class = PurchaseOrderShippingSerializer

class PurchaseOrderShippingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrderShipping.objects.all()
    serializer_class = PurchaseOrderShippingSerializer
    lookup_field = 'slug'


''' VISTAS: Búsqueda de productos. '''
class ProductSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'sku'

    filter_backends = [ filters.SearchFilter ]
    search_fields = [ 'name', 'sku' ]

''' VISTAS: Inicio de sesión. '''
class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({'error': 'Ingrese su usuario.'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Ingrese su contraseña.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response({'error': 'Cuenta de usuario desactivada.'}, status=status.HTTP_401_UNAUTHORIZED)

            login(request, user)

            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return Response({'message': 'Inicio de sesión exitoso', 'user': data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuario o contraseña incorrectos.'}, status=status.HTTP_401_UNAUTHORIZED)