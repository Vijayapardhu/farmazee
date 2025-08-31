from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Vendor(models.Model):
    """Vendor model for marketplace sellers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=200)
    business_description = models.TextField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    pan_number = models.CharField(max_length=20, blank=True, null=True)
    business_license = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_orders = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')
    
    def __str__(self):
        return self.business_name


class ProductCategory(models.Model):
    """Product category model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model for marketplace"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)
    min_order_quantity = models.IntegerField(default=1)
    max_order_quantity = models.IntegerField(default=100)
    unit = models.CharField(max_length=20, default='kg', help_text='Unit of measurement (kg, pieces, etc.)')
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text='Weight in kg')
    dimensions = models.CharField(max_length=100, blank=True, null=True, help_text='Length x Width x Height in cm')
    
    # Product details
    brand = models.CharField(max_length=100, blank=True, null=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)
    warranty = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    # Status and visibility
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_organic = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)
    
    # SEO and marketing
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True)
    
    # Statistics
    views = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.vendor.business_name}"
    
    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.price
    
    @property
    def discount_percentage(self):
        if self.sale_price and self.price:
            return round(((self.price - self.sale_price) / self.price) * 100, 2)
        return 0


class ProductImage(models.Model):
    """Product images model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


# Input & Resource Management Models
class InputCategory(models.Model):
    """Input category model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Input Categories'
    
    def __str__(self):
        return self.name


class Input(models.Model):
    """Agricultural inputs model"""
    INPUT_TYPES = [
        ('seeds', 'Seeds'),
        ('fertilizers', 'Fertilizers'),
        ('pesticides', 'Pesticides'),
        ('herbicides', 'Herbicides'),
        ('fungicides', 'Fungicides'),
        ('irrigation', 'Irrigation Equipment'),
        ('tools', 'Tools & Equipment'),
        ('machinery', 'Machinery'),
        ('organic', 'Organic Inputs'),
        ('other', 'Other'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='inputs')
    category = models.ForeignKey(InputCategory, on_delete=models.CASCADE, related_name='inputs')
    input_type = models.CharField(max_length=20, choices=INPUT_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20, default='kg')
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Input specifications
    composition = models.TextField(blank=True, null=True)
    application_rate = models.CharField(max_length=100, blank=True, null=True)
    suitable_crops = models.TextField(blank=True, null=True)
    safety_instructions = models.TextField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_organic = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)
    
    # Statistics
    views = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_input_type_display()}"


class InputImage(models.Model):
    """Input images model"""
    input_item = models.ForeignKey(Input, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='inputs/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.input_item.name} - Image {self.order}"


class Resource(models.Model):
    """Resource management model"""
    RESOURCE_TYPES = [
        ('land', 'Land'),
        ('water', 'Water'),
        ('labor', 'Labor'),
        ('equipment', 'Equipment'),
        ('storage', 'Storage'),
        ('transport', 'Transport'),
        ('financial', 'Financial'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    location = models.CharField(max_length=200, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    maintenance_schedule = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_resource_type_display()}"


class Inventory(models.Model):
    """Inventory management model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    input_item = models.ForeignKey(Input, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-purchase_date']
        verbose_name_plural = 'Inventories'
    
    def __str__(self):
        item_name = self.product.name if self.product else self.input_item.name
        return f"{item_name} - {self.quantity} {self.unit}"


class Order(models.Model):
    """Order model for marketplace"""
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Shipping information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=10)
    shipping_phone = models.CharField(max_length=15)
    
    # Order status
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Payment information
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    order_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"


class OrderItem(models.Model):
    """Order items model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    input_item = models.ForeignKey(Input, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        item_name = self.product.name if self.product else self.input_item.name
        return f"{item_name} - {self.quantity}"


class Review(models.Model):
    """Product/Input reviews model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='reviews')
    input_item = models.ForeignKey(Input, on_delete=models.CASCADE, blank=True, null=True, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        item_name = self.product.name if self.product else self.input_item.name
        return f"{item_name} - {self.rating} stars by {self.user.username}"
