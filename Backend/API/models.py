
from django.db import models


# MODELO: Productos
class Product(models.Model):
    sku = models.CharField(max_length=16, unique=True,
        verbose_name='Código (SKU)', help_text='Código de identificación único del producto')
    name = models.CharField(max_length=64,
        verbose_name='Nombre', help_text='Nombre del producto')
    description = models.TextField(max_length=256,
        verbose_name='Descripción', help_text='Descripción corta del producto')
    price = models.DecimalField(max_digits=8, decimal_places=2,
        verbose_name='Precio', help_text='Precio unitario del producto')
    stock = models.PositiveIntegerField(default=0,
        verbose_name='Stock', help_text='Cantidad disponible del producto')
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name


# MODELO: Proveedores
class Supplier(models.Model):
    name = models.CharField(max_length=64, unique=True, 
        verbose_name='Nombre', help_text='Nombre único del proveedor')
    description = models.TextField(max_length=256,
        verbose_name='Descripción', help_text='Descripción del proveedor')
    shipping = models.DecimalField(max_digits=10, decimal_places=2,
        verbose_name='Envío', help_text='Coste de envío por orden de compra')

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.name


# MODELO: Productos del proveedor.
class SupplierProducts(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='discounts',
        verbose_name='Proveedor', help_text='Proveedor que aplica el descuento')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts',
        verbose_name='Producto', help_text='Producto al que se aplica el descuento')
    minimum = models.PositiveIntegerField(default=0, verbose_name='Cantidad mínima',
        help_text='Cantidad mínima del mismo producto necesaria para aplicar el descuento')
    discount = models.DecimalField(max_digits=4, decimal_places=2,
        verbose_name='Descuento', help_text='Porcentaje de descuento a aplicar al producto')

    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        unique_together = ('supplier', 'product', 'minimum')

    def __str__(self):
        return f'Desc. {self.discount}% para {self.product.name} ({self.minimum} mínimo) - {self.supplier.name}'


# MODELO: Órdenes de Compra
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Procesando', 'Procesando'),
        ('Procesando', 'Procesando'),
        ('Cancelada', 'Cancelada'),
    ]

    purchaser = models.CharField(max_length=64,
        verbose_name='Comprador', help_text='Nombre del comprador')
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0,
        verbose_name='Costo de envío', help_text='Costo de envío para este producto en la orden')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,
        verbose_name='Subtotal', help_text='Subtotal del costo del pedido')
    discount = models.DecimalField(max_digits=10, decimal_places=2,
        verbose_name='Descuento', help_text='Suma total del descuento aplicado al pedido')
    iva = models.DecimalField(max_digits=4, decimal_places=2, default=16.00,
        verbose_name='Impuestos (IVA %)', help_text='Suma total de impuestos aplicados al pedido')
    total = models.DecimalField(max_digits=10, decimal_places=2,
        verbose_name='Total', help_text='Costo total del pedido')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Pendiente',
        verbose_name='Estado', help_text='Estado actual de la orden')
    order_date = models.DateTimeField(auto_now_add=True,
        verbose_name='Fecha de pedido', help_text='Fecha en que se realizó el pedido')
    
    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'

    def __str__(self):
        return f'Orden de compra No. {self.id}'


# MODELO: Ítems de la Orden de Compra
class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True,
        related_name='items', verbose_name='Orden de compra', help_text='Orden a la que pertenece este producto')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
        verbose_name='Producto', help_text='Producto solicitado en la orden de compra')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True,
        verbose_name='Proveedor', help_text='Proveedor del producto')
    quantity = models.PositiveIntegerField(default=0,
        verbose_name='Cantidad', help_text='Número de unidades solicitadas del producto')
    unit_price = models.DecimalField(max_digits=8, decimal_places=2,
        verbose_name='Precio unitario', help_text='Precio por unidad del producto en esta orden')
    discount_applied = models.DecimalField(max_digits=5, decimal_places=2, default=0,
        verbose_name='Descuento aplicado (%)', help_text='Porcentaje de descuento aplicado al producto en esta orden')

    class Meta:
        verbose_name = 'Ítem de Orden'
        verbose_name_plural = 'Ítems de Orden'
    
    def __str__(self):
        return f'Orden No. {self.id} ({self.product.name})'