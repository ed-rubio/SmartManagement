
from .models import *
from rest_framework import serializers


# SERIALIZADOR: Productos.
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='Product (Detail/Update/Delete)', lookup_field='sku')
    sku = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=256)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    stock = serializers.IntegerField()

    class Meta:
        model = Product
        fields = [ 'url', 'sku', 'name', 'description', 'price', 'stock' ]
        lookup_field = 'sku'

    # Validación: El precio debe ser mayor a cero.
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio del producto no puede ser igual o menor a cero.')
        return value

    # Validación: El stock debe ser mayor o igual a cero.
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock del producto no puede ser menor a cero.')
        return value


# ...