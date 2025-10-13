from django.contrib import admin
from .models import (
    Vendor, ProductCategory, Product, ProductImage, InputCategory, Input, InputImage,
    Resource, Inventory, Order, OrderItem, Review, MarketPrice
)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'city', 'state', 'is_verified', 'is_active', 'rating', 'total_orders']
    list_filter = ['is_verified', 'is_active', 'rating']
    search_fields = ['business_name', 'user__username', 'city', 'state']
    list_editable = ['is_verified', 'is_active']
    readonly_fields = ['rating', 'total_orders', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Business Information', {
            'fields': ('user', 'business_name', 'business_description')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'city', 'state', 'pincode')
        }),
        ('Business Details', {
            'fields': ('gst_number', 'pan_number', 'business_license')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Statistics', {
            'fields': ('rating', 'total_orders')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'category', 'price', 'current_price', 'stock_quantity', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'is_organic', 'is_certified']
    search_fields = ['name', 'description', 'vendor__business_name']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['views', 'sales_count', 'rating', 'review_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('vendor', 'category', 'name', 'description', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'min_order_quantity', 'max_order_quantity', 'unit')
        }),
        ('Product Details', {
            'fields': ('brand', 'model_number', 'warranty', 'expiry_date', 'weight', 'dimensions')
        }),
        ('Specifications', {
            'fields': ('is_organic', 'is_certified')
        }),
        ('SEO & Marketing', {
            'fields': ('meta_title', 'meta_description', 'tags')
        }),
        ('Statistics', {
            'fields': ('views', 'sales_count', 'rating', 'review_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'is_primary', 'alt_text']
    list_filter = ['is_primary', 'order']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['order', 'is_primary']

@admin.register(InputCategory)
class InputCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']

@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'category', 'input_type', 'price', 'stock_quantity', 'is_featured', 'is_active']
    list_filter = ['category', 'input_type', 'is_featured', 'is_active', 'is_organic', 'is_certified']
    search_fields = ['name', 'description', 'vendor__business_name']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['views', 'sales_count', 'rating', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('vendor', 'category', 'input_type', 'name', 'description', 'brand', 'model')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'sale_price', 'stock_quantity', 'unit', 'weight')
        }),
        ('Specifications', {
            'fields': ('composition', 'application_rate', 'suitable_crops', 'safety_instructions', 'expiry_date')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active', 'is_organic', 'is_certified')
        }),
        ('Statistics', {
            'fields': ('views', 'sales_count', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(InputImage)
class InputImageAdmin(admin.ModelAdmin):
    list_display = ['input_item', 'order', 'is_primary', 'alt_text']
    list_filter = ['is_primary', 'order']
    search_fields = ['input_item__name', 'alt_text']
    list_editable = ['order', 'is_primary']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'resource_type', 'quantity', 'unit', 'location', 'is_active']
    list_filter = ['resource_type', 'is_active']
    search_fields = ['name', 'description', 'user__username', 'location']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Resource Information', {
            'fields': ('user', 'resource_type', 'name', 'description')
        }),
        ('Quantity & Location', {
            'fields': ('quantity', 'unit', 'location')
        }),
        ('Financial', {
            'fields': ('cost', 'purchase_date')
        }),
        ('Maintenance', {
            'fields': ('maintenance_schedule',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'input_item', 'quantity', 'unit', 'purchase_date', 'purchase_price']
    list_filter = ['purchase_date']
    search_fields = ['user__username', 'product__name', 'input_item__name', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Inventory Information', {
            'fields': ('user', 'product', 'input_item')
        }),
        ('Quantity & Pricing', {
            'fields': ('quantity', 'unit', 'purchase_price')
        }),
        ('Dates', {
            'fields': ('purchase_date', 'expiry_date')
        }),
        ('Location & Notes', {
            'fields': ('location', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'final_amount', 'order_status', 'payment_status', 'order_date']
    list_filter = ['order_status', 'payment_status', 'order_date']
    search_fields = ['order_number', 'customer__username', 'shipping_address']
    list_editable = ['order_status', 'payment_status']
    readonly_fields = ['order_date', 'payment_date', 'shipped_date', 'delivered_date']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'order_number', 'total_amount', 'shipping_amount', 'tax_amount', 'discount_amount', 'final_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_pincode', 'shipping_phone')
        }),
        ('Status', {
            'fields': ('order_status', 'payment_status')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('order_date', 'payment_date', 'shipped_date', 'delivered_date')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'input_item', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__order_status']
    search_fields = ['order__order_number', 'product__name', 'input_item__name']
    readonly_fields = ['total_price']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'input_item', 'rating', 'title', 'is_verified_purchase', 'is_approved']
    list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
    search_fields = ['user__username', 'title', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'product', 'input_item', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'mandi_name', 'price_per_quintal', 'price_date', 'change_percentage', 'volume', 'is_current']
    list_filter = ['crop', 'mandi_name', 'price_date', 'is_current']
    search_fields = ['crop__name', 'mandi_name']
    list_editable = ['is_current']
    readonly_fields = ['change_percentage', 'created_at', 'updated_at']
    date_hierarchy = 'price_date'
    
    fieldsets = (
        ('Price Information', {
            'fields': ('crop', 'mandi_name', 'price_per_quintal', 'price_date')
        }),
        ('Market Data', {
            'fields': ('change_percentage', 'volume', 'is_current')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Auto-calculate change percentage if not provided
        if not change and not obj.change_percentage:
            previous_price = MarketPrice.objects.filter(
                crop=obj.crop, 
                mandi_name=obj.mandi_name
            ).exclude(id=obj.id).order_by('-price_date').first()
            
            if previous_price:
                obj.change_percentage = ((obj.price_per_quintal - previous_price.price_per_quintal) / 
                                       previous_price.price_per_quintal) * 100
        
        super().save_model(request, obj, form, change)
