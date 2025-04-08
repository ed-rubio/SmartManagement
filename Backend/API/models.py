
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


''' MODELO: Almacenes. '''
class Warehouse(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT,
        verbose_name='Propietario', help_text='Propietario del almacén')
    name = models.CharField(max_length=64,
        verbose_name='Nombre', help_text='Nombre del almacén')
    description = models.TextField(max_length=256,
        verbose_name='Descripción', help_text='Descripción del almacén')
    slug = models.SlugField(default='', null=True, blank=True,
        verbose_name='Slug', help_text='Slug del almacén')

    class Meta:
        verbose_name = 'Almacén'
        verbose_name_plural = 'Almacenes'
        unique_together = ( 'owner', 'name' )

    def __str__(self):
        return f'{self.name} ({self.owner.username})'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'WH-{self.name}-OWN-{self.owner.username}')
        super(Warehouse, self).save(*args, **kwargs)


''' MODELO: Proveedores. '''
class Supplier(models.Model):
    name = models.CharField(max_length=64, unique=True, 
        verbose_name='Nombre', help_text='Nombre único del proveedor')
    description = models.TextField(max_length=256,
        verbose_name='Descripción', help_text='Descripción del proveedor')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        verbose_name='Tarifa de envío', help_text='Costo estándar por envío de mercancía')
    slug = models.SlugField(default='', null=True, blank=True,
        verbose_name='Slug', help_text='Slug del proveedor')

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Supplier, self).save(*args, **kwargs)


''' MODELO: Productos. '''
class Product(models.Model):
    sku = models.CharField(max_length=16, unique=True,
        verbose_name='Código (SKU)', help_text='Código del producto')
    name = models.CharField(max_length=64,
        verbose_name='Nombre', help_text='Nombre del producto')
    description = models.TextField(max_length=256,
        verbose_name='Descripción', help_text='Descripción corta del producto')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,
        verbose_name='Proveedor', help_text='Proveedor del producto')
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0,
        verbose_name='Costo', help_text='Costo unitario del producto')
    iva = models.DecimalField(max_digits=4, decimal_places=2, default=0,
        verbose_name='Impuestos (IVA %)', help_text='Porcentaje de IVA del producto')
    ieps = models.DecimalField(max_digits=4, decimal_places=2, default=0,
        verbose_name='Impuestos (IEPS %)', help_text='Porcentaje de IEPS del producto')
    slug = models.SlugField(default='', null=True, blank=True,
        verbose_name='Slug', help_text='Slug del producto')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'{self.name} ({self.supplier.name})'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sku)
        super(Product, self).save(*args, **kwargs)


''' MODELO: Productos en almacén. '''
class WarehouseProducts(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT,
        verbose_name='Almacén', help_text='Almacén en el que se tendrá el producto')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
        verbose_name='Producto', help_text='Producto a almacenar')
    product_state = models.BooleanField(default=True,
        verbose_name='Estado', help_text='Estado del producto (True=Activo, False=Inactivo)')
    product_stock = models.PositiveIntegerField(default=0,
        verbose_name='Stock', help_text='Stock disponible del producto')
    slug = models.SlugField(default='', null=True, blank=True,
        verbose_name='Slug', help_text='Slug del producto a almacenar')

    class Meta:
        verbose_name = 'Producto almacenado'
        verbose_name_plural = 'Productos almacenados'
        unique_together = ( 'warehouse', 'product' )

    def __str__(self):
        return f'{self.product.name}: {self.warehouse.name} ({self.warehouse.owner.username})'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'WH-{self.warehouse.name}-OWN-{self.warehouse.owner.username}-SKU-{self.product.sku}')
        super(WarehouseProducts, self).save(*args, **kwargs)


''' MODELO: Órdenes de compra. '''
class PurchaseOrder(models.Model):
    purchaser = models.ForeignKey(User, on_delete=models.PROTECT,
        verbose_name='Comprador', help_text='Usuario que realiza la orden de compra')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        verbose_name='Costo de envío', help_text='Suma total de costos de envío')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        verbose_name='Subtotal', help_text='Suma del precio unitario de los productos')
    iva_total = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        verbose_name='IVA (total)', help_text='Suma del IVA de los productos')
    ieps_total = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        verbose_name='IEPS (total)', help_text='Suma del IEPS de los productos')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        verbose_name='Total', help_text='Costo total de la orden de compra')
    order_date = models.DateTimeField(default=timezone.now, null=True, blank=True,
        verbose_name='Fecha de orden', help_text='Fecha en que se realiza la orden de compra')
    slug = models.SlugField(default='', null=True, blank=True,
        verbose_name='Slug', help_text='Slug de la orden de compra')

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Órdenes de compra'

    def __str__(self):
        return f'Orden #{self.id} ({self.purchaser.username}): {self.order_date.strftime("%B %d, %Y: %I:%M%p")}'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'PRCH-{self.purchaser.username}-DT-{timezone.now()}')
        super(PurchaseOrder, self).save(*args, **kwargs)
        self._calculate_totals() 
    
    # Realiza un cálculo automático de los totales.
    def _calculate_totals(self):
        subtotal = Decimal('0.00')
        iva_total = Decimal('0.00')
        ieps_total = Decimal('0.00')
        shipping_cost_total = Decimal('0.00')

        for item in PurchaseOrderProducts.objects.filter(purchase_order=self):
            subtotal += item.unit_cost * item.quantity
            iva_total += (item.unit_cost * item.quantity) * (item.iva / 100)
            ieps_total += (item.unit_cost * item.quantity) * (item.ieps / 100)

        for shipping in PurchaseOrderShipping.objects.filter(purchase_order=self):
            shipping_cost_total += shipping.shipping_cost

        self.subtotal = subtotal
        self.iva_total = iva_total
        self.ieps_total = ieps_total
        self.shipping_cost = shipping_cost_total
        self.total = subtotal + iva_total + ieps_total + shipping_cost_total
        super().save() # Guarda los totales actualizados. :)


''' MODELO: Productos (OC-R). '''
class PurchaseOrderProducts(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,
        verbose_name='Orden de compra', help_text='Orden de compra del producto')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
        verbose_name='Producto', help_text='Producto a incluir')
    quantity = models.PositiveIntegerField(default=1,
        verbose_name='Cantidad', help_text='Cantidad pedida')
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2,
        verbose_name='Costo', help_text='Costo unitario del producto')
    iva = models.DecimalField(max_digits=4, decimal_places=2,
        verbose_name='IVA (%)', help_text='Porcentaje de IVA del producto')
    ieps = models.DecimalField(max_digits=4, decimal_places=2,
        verbose_name='IEPS (%)', help_text='Porcentaje de IEPS del producto')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0,
        verbose_name='Importe', help_text='Importe total del producto')
    slug = models.SlugField(default='', null=True, blank=True,
        verbose_name='Slug', help_text='Slug del producto en la orden de compra')

    class Meta:
        verbose_name = 'Producto (OC-R)'
        verbose_name_plural = 'Productos (OC-R)'
        unique_together = ( 'purchase_order', 'product' )

    def __str__(self):
        return f'Orden No. {self.purchase_order.id}: {self.product.name} ({self.quantity})'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'PRD-{self.product.sku}-ORD-{self.purchase_order.id}')
        super(PurchaseOrderProducts, self).save(*args, **kwargs)


''' MODELO: Costos de envío (OC-R). '''
class PurchaseOrderShipping(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,
        verbose_name='Orden de compra', help_text='Orden de compra del envío')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,
        verbose_name='Proveedor', help_text='Proveedor que realiza el envío')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        verbose_name='Costo de envío', help_text='Costo total del envío')
    slug = models.SlugField(default='', null=True, blank=True,
        verbose_name='Slug', help_text='Slug del costo de envío en la orden de compra')

    class Meta:
        verbose_name = 'Costo de envío (OC-R)'
        verbose_name_plural = 'Costos de envío (OC-R)'
        unique_together = ( 'purchase_order', 'supplier' )

    def __str__(self):
        return f'Orden No. {self.purchase_order.id}: {self.supplier.name} (${self.shipping_cost})'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'SPL-{self.supplier.name}-ORD-{self.purchase_order.id}')
        super(PurchaseOrderShipping, self).save(*args, **kwargs)