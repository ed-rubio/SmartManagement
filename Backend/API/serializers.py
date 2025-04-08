
from .models import *
from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from django.core.validators import MinValueValidator
from rest_framework.validators import UniqueValidator


''' SERIALIZADOR: Almacenes. '''
class WarehouseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='Warehouse (Detail/Update/Delete)', lookup_field='slug',
        help_text='URL única para acceder a este almacén en la API.')
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
        label='Propietario', help_text='Propietario del almacén')
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    name = serializers.CharField(max_length=64,
        label='Nombre', help_text='Nombre del almacén')
    description = serializers.CharField(max_length=256,
        label='Descripción', help_text='Descripción del almacén')
    slug = serializers.CharField(read_only=True, label='Slug', help_text='Slug del almacén')

    class Meta:
        model = Warehouse
        fields = [ 'url', 'owner', 'owner_username', 'name', 'description', 'slug' ]
        lookup_field = 'slug'
        validators = []

    ''' Validación: Unicidad combinada de propietario y nombre del almacén. '''
    def validate(self, attrs):
        owner = attrs.get('owner') # Propietario del almacén.
        name = attrs.get('name') # Nombre del almacén.
        instance = getattr(self, 'instance', None) # Instancia del almacén (si se está actualizando).

        if owner and name: # Verificación de unicidad: propietario/nombre.
            warehouse = Warehouse.objects.filter(owner=owner, name=name)

            if instance: # Al actualizar, excluye la instancia actual de la verificación.
                warehouse = warehouse.exclude(pk=instance.pk)

            if warehouse.exists():
                raise serializers.ValidationError({'name': f'{owner.username} posee un almacén con el mismo nombre.'})
        return attrs


''' SERIALIZADOR: Proveedores. '''
class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='Supplier (Detail/Update/Delete)', lookup_field='slug',
        help_text='URL única para acceder a este proveedor en la API.')
    name = serializers.CharField(max_length=64,
        label='Nombre', help_text='Nombre único del proveedor',
        validators=[UniqueValidator(queryset=Supplier.objects.all(), message='Ya existe un proveedor con este nombre.')])
    description = serializers.CharField(max_length=256,
        label='Descripción', help_text='Descripción del proveedor')
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2,
        label='Tarifa de envío', help_text='Costo estándar por envío de mercancía',
        validators=[MinValueValidator(Decimal('0.01'), message='El costo de envío no puede ser menor o igual a cero.')])
    slug = serializers.CharField(read_only=True, label='Slug', help_text='Slug del proveedor')

    class Meta:
        model = Supplier
        fields = [ 'url', 'name', 'description', 'shipping_cost', 'slug' ]
        lookup_field = 'slug'


''' SERIALIZADOR: Productos. '''
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='Product (Detail/Update/Delete)', lookup_field='sku',
        help_text='URL única para acceder a este producto en la API.')
    sku = serializers.CharField(max_length=16,
        label='Código (SKU)', help_text='Código del producto',
        validators=[UniqueValidator(queryset=Product.objects.all(), message='Ya existe un producto con este SKU.')])
    name = serializers.CharField(max_length=64,
        label='Nombre', help_text='Nombre del producto')
    description = serializers.CharField(max_length=256,
        label='Descripción', help_text='Descripción corta del producto')
    supplier = serializers.HyperlinkedRelatedField(view_name='Supplier (Detail/Update/Delete)', lookup_field='slug',
        label='Proveedor', help_text='Proveedor que realiza el envío', queryset=Supplier.objects.all())
    cost = serializers.DecimalField(max_digits=8, decimal_places=2,
        label='Costo', help_text='Costo unitario del producto',
        validators=[MinValueValidator(Decimal('0.01'), message='El costo del producto no puede ser menor o igual a cero.')])
    iva = serializers.DecimalField(max_digits=4, decimal_places=2,
        label='Impuestos (IVA %)', help_text='Porcentaje de IVA del producto',
        validators=[MinValueValidator(Decimal('0.00'), message='El porcentaje de IVA aplicado no puede ser menor a cero.')])
    ieps = serializers.DecimalField(max_digits=4, decimal_places=2,
        label='Impuestos (IEPS %)', help_text='Porcentaje de IEPS del producto',
        validators=[MinValueValidator(Decimal('0.00'), message='El porcentaje de IEPS aplicado no puede ser menor a cero.')])
    slug = serializers.CharField(read_only=True, label='Slug', help_text='Slug del producto')

    class Meta:
        model = Product
        fields = [ 'url', 'sku', 'name', 'description', 'supplier', 'cost', 'iva', 'ieps', 'slug' ]
        lookup_field = 'sku'


''' SERIALIZADOR: Productos en almacén. '''
class WarehouseProductsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='WarehouseProducts (Detail/Update/Delete)', lookup_field='slug',
        help_text='URL única para acceder a este "producto en almacén" en la API.')
    warehouse = serializers.HyperlinkedRelatedField(view_name='Warehouse (Detail/Update/Delete)', lookup_field='slug',
        label='Almacén', help_text='Almacén en el que se tendrá el producto', queryset=Warehouse.objects.all())
    product = serializers.HyperlinkedRelatedField(view_name='Product (Detail/Update/Delete)', lookup_field='sku',
        label='Producto', help_text='Producto a almacenar', queryset=Product.objects.all())
    product_state = serializers.BooleanField(label='Estado', help_text='Estado del producto (True=Activo, False=Inactivo)')
    product_stock = serializers.IntegerField(label='Stock', help_text='Stock disponible del producto',
        validators=[MinValueValidator(0, message='El stock del producto no puede ser menor a cero.')])
    slug = serializers.CharField(read_only=True, label='Slug', help_text='Slug del producto a almacenar')

    class Meta:
        model = WarehouseProducts
        fields = [ 'url', 'warehouse', 'product', 'product_state', 'product_stock', 'slug' ]
        lookup_field = 'slug'
        validators = []

    ''' Validación: Unicidad combinada de almacén y producto. '''
    def validate(self, attrs):
        warehouse = attrs.get('warehouse') # Almacén.
        product = attrs.get('product') # Producto.
        instance = getattr(self, 'instance', None) # Instancia (si se está actualizando).

        if warehouse and product: # Verificación de unicidad: almacén/producto.
            warehouse_product = WarehouseProducts.objects.filter(warehouse=warehouse, product=product)

            if instance: # Al actualizar, excluye la instancia actual de la verificación.
                warehouse_product = warehouse_product.exclude(pk=instance.pk)

            if warehouse_product.exists():
                raise serializers.ValidationError({'product': f'El producto ya se encuentra registrado en este almacén.'})
        return attrs


''' SERIALIZADOR: Órdenes de compra. '''
class PurchaseOrderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='PurchaseOrder (Detail/Update/Delete)', lookup_field='slug',
        help_text='URL única para acceder a esta orden de compra en la API.')
    purchaser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
        label='Comprador', help_text='Usuario que realiza la orden de compra')
    purchaser_username = serializers.CharField(source='purchaser.username', read_only=True)
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2,
        label='Costo de envío', help_text='Suma total de costos de envío', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2,
        label='Subtotal', help_text='Suma del precio unitario de los productos', read_only=True)
    iva_total = serializers.DecimalField(max_digits=10, decimal_places=2,
        label='IVA (total)', help_text='Suma del IVA de los productos', read_only=True)
    ieps_total = serializers.DecimalField(max_digits=10, decimal_places=2,
        label='IEPS (total)', help_text='Suma del IEPS de los productos', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2,
        label='Total', help_text='Costo total de la orden de compra', read_only=True)
    order_date = serializers.DateTimeField(read_only=True,
        label='Fecha de orden', help_text='Fecha en que se realiza la orden de compra')
    order_products = serializers.SerializerMethodField()
    order_shipping_costs = serializers.SerializerMethodField()
    slug = serializers.CharField(read_only=True, label='Slug', help_text='Slug de la orden de compra')

    class Meta:
        model = PurchaseOrder
        fields = [ 'url', 'purchaser', 'purchaser_username', 'shipping_cost', 'subtotal', 'iva_total',
            'ieps_total', 'total', 'order_date', 'order_products', 'order_shipping_costs', 'slug' ]
        lookup_field = 'slug'

    def get_order_products(self, instance):
        order_products = PurchaseOrderProducts.objects.filter(purchase_order=instance)
        serializer = PurchaseOrderProductsSerializer(order_products, many=True, context=self.context)
        return serializer.data

    def get_order_shipping_costs(self, instance):
        order_shipping_costs = PurchaseOrderShipping.objects.filter(purchase_order=instance)
        serializer = PurchaseOrderShippingSerializer(order_shipping_costs, many=True, context=self.context)
        return serializer.data


''' SERIALIZADOR: Productos (OC-R). '''
class PurchaseOrderProductsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='PurchaseOrderProducts (Detail/Update/Delete)', lookup_field='slug',
        help_text='URL única para acceder al producto (OC-R) en la API.')
    purchase_order = serializers.HyperlinkedRelatedField(view_name='PurchaseOrder (Detail/Update/Delete)', lookup_field='slug',
        label='Orden de compra', help_text='Orden de compra del producto', queryset=PurchaseOrder.objects.all())
    product = serializers.HyperlinkedRelatedField(view_name='Product (Detail/Update/Delete)', lookup_field='sku',
        label='Producto', help_text='Producto a incluir', queryset=Product.objects.all())
    product_name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(label='Cantidad', help_text='Cantidad pedida',
        validators=[MinValueValidator(1, message='La cantidad pedida no puede ser menor o igual a cero.')])
    unit_cost = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True,
        label='Costo', help_text='Costo unitario del producto')
    iva = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True,
        label='IVA (total)', help_text='Total de IVA del producto')
    ieps = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True,
        label='IEPS (total)', help_text='Total de IEPS del producto')
    total = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True,
        label='Importe', help_text='Importe total del producto')
    slug = serializers.CharField(read_only=True, label='Slug', help_text='Slug del producto en la orden de compra')

    class Meta:
        model = PurchaseOrderProducts
        fields = [ 'url', 'purchase_order', 'product', 'product_name', 'quantity', 'unit_cost', 'iva', 'ieps', 'total', 'slug' ]
        lookup_field = 'slug'
        validators = []

    ''' Creación: Calcula valores automáticamente, actualización de OC-R. '''
    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        purchase_order = validated_data['purchase_order']

        validated_data['unit_cost'] = product.cost
        validated_data['iva'] = product.iva
        validated_data['ieps'] = product.ieps

        iva_amount = quantity * product.cost * (product.iva / 100)
        ieps_amount = quantity * product.cost * (product.ieps / 100)
        validated_data['total'] = (quantity * product.cost) + iva_amount + ieps_amount

        purchase_order_product = super().create(validated_data)

        if purchase_order:
            try: # Actualiza los totales de la OC-R asociada.
                instance = purchase_order
                instance._calculate_totals()

                if product.supplier and not PurchaseOrderShipping.objects.filter(
                    purchase_order=purchase_order, supplier=product.supplier
                ).exists():
                    PurchaseOrderShipping.objects.create(
                        purchase_order=purchase_order,
                        supplier=product.supplier,
                        shipping_cost=product.supplier.shipping_cost
                    )

                    instance._calculate_totals()

            except PurchaseOrder.DoesNotExist:
                raise NotFound(detail=f'La orden de compra no existe.')

        return purchase_order_product

    ''' Actualización: Calcula valores automáticamente, actualización de OC-R. '''
    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', instance.quantity)

        validated_data['unit_cost'] = instance.product.cost
        validated_data['iva'] = instance.product.iva
        validated_data['ieps'] = instance.product.ieps

        iva_amount = quantity * instance.product.cost * (instance.product.iva / 100)
        ieps_amount = quantity * instance.product.cost * (instance.product.ieps / 100)
        validated_data['total'] = (quantity * instance.product.cost) + iva_amount + ieps_amount

        purchase_order_product = super().update(instance, validated_data)

        if purchase_order_product.purchase_order:
            try: # Actualiza los totales de la OC-R asociada.
                purchase_order_instance = purchase_order_product.purchase_order
                purchase_order_instance._calculate_totals()
            except PurchaseOrder.DoesNotExist:
                raise NotFound(detail=f'La orden de compra no existe.')

        return purchase_order_product

    ''' Validación: Unicidad combinada de orden de compra y producto. '''
    def validate(self, attrs):
        purchase_order = attrs.get('purchase_order') # Orden de compra.
        product = attrs.get('product') # Producto.
        instance = getattr(self, 'instance', None) # Instancia (si se está actualizando).

        if purchase_order and product: # Verificación de unicidad: orden de compra/producto.
            item = PurchaseOrderProducts.objects.filter(purchase_order=purchase_order, product=product)

            if instance: # Al actualizar, excluye la instancia actual de la verificación.
                item = item.exclude(pk=instance.pk)
            if item.exists():
                raise serializers.ValidationError({'product': f'El producto ya se encuentra en esta orden de compra.'})
        return attrs


''' SERIALIZADOR: Costos de envío (OC-R). '''
class PurchaseOrderShippingSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='PurchaseOrderShipping (Detail/Update/Delete)', lookup_field='slug',
        help_text='URL única para acceder a este costo de envío (OC-R) en la API.')
    purchase_order = serializers.HyperlinkedRelatedField(view_name='PurchaseOrder (Detail/Update/Delete)', lookup_field='slug',
        label='Orden de compra', help_text='Orden de compra del envío', queryset=PurchaseOrder.objects.all())
    supplier = serializers.HyperlinkedRelatedField(view_name='Supplier (Detail/Update/Delete)', lookup_field='slug',
        label='Proveedor', help_text='Proveedor que realiza el envío', queryset=Supplier.objects.all())
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2,
        label='Costo de envío', help_text='Costo total del envío')
    slug = serializers.CharField(read_only=True, label='Slug', help_text='Slug del costo de envío en la orden de compra')

    class Meta:
        model = PurchaseOrderShipping
        fields = [ 'url', 'purchase_order', 'supplier', 'supplier_name', 'shipping_cost', 'slug' ]
        lookup_field = 'slug'

    ''' Creación: Calcula valores automáticamente, actualización de la OC-R. '''
    def create(self, validated_data):
        supplier = validated_data['supplier']
        validated_data['shipping_cost'] = supplier.shipping_cost
        purchase_order_shipping = super().create(validated_data)

        if purchase_order_shipping.purchase_order:
            try: # Actualiza los totales de la OC-R asociada.
                instance = purchase_order_shipping.purchase_order
                instance._calculate_totals()
            except PurchaseOrder.DoesNotExist:
                raise NotFound(detail=f'La orden de compra no existe.')

        return purchase_order_shipping

    ''' Actualización: Calcula valores automáticamente, actualización de la OC-R. '''
    def update(self, instance, validated_data):
        supplier = validated_data.get('supplier')

        if supplier:
            validated_data['shipping_cost'] = supplier.shipping_cost

        purchase_order_shipping = super().update(instance, validated_data)

        if purchase_order_shipping.purchase_order:
            try: # Actualiza los totales de la OC-R asociada.
                purchase_order_instance = purchase_order_shipping.purchase_order
                purchase_order_instance._calculate_totals()
            except PurchaseOrder.DoesNotExist:
                raise NotFound(detail=f'La orden de compra no existe.')

        return purchase_order_shipping

    ''' Validación: Unicidad combinada de orden de compra y proveedor. '''
    def validate(self, attrs):
        purchase_order = attrs.get('purchase_order') # Orden de compra.
        supplier = attrs.get('supplier') # Proveedor.
        instance = getattr(self, 'instance', None) # Instancia (si se está actualizando).

        if purchase_order and supplier: # Verificación de unicidad: orden de compra/proveedor.
            item = PurchaseOrderShipping.objects.filter(purchase_order=purchase_order, supplier=supplier)

            if instance: # Al actualizar, excluye la instancia actual de la verificación.
                item = item.exclude(pk=instance.pk)

            if item.exists():
                raise serializers.ValidationError({'supplier': f'El proveedor ya se encuentra registrado en esta orden de compra.'})
        return attrs