from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductCategory, Order, OrderItem, Vendor, Input, InputCategory


def marketplace_home(request):
    """Marketplace home page"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = ProductCategory.objects.filter(is_active=True)[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'marketplace/home.html', context)


def product_list(request):
    """List all products"""
    products = Product.objects.filter(is_active=True)
    context = {'products': products}
    return render(request, 'marketplace/products.html', context)


def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    context = {'product': product}
    return render(request, 'marketplace/product_detail.html', context)


def category_products(request, pk):
    """Products by category"""
    category = get_object_or_404(ProductCategory, pk=pk, is_active=True)
    products = category.products.filter(is_active=True)
    context = {'category': category, 'products': products}
    return render(request, 'marketplace/category_products.html', context)


@login_required
def order_list(request):
    """User's order list"""
    orders = Order.objects.filter(customer=request.user)
    context = {'orders': orders}
    return render(request, 'marketplace/orders.html', context)


@login_required
def order_detail(request, pk):
    """Order detail view"""
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    context = {'order': order}
    return render(request, 'marketplace/order_detail.html', context)


@login_required
def vendor_dashboard(request):
    """Vendor dashboard"""
    if not hasattr(request.user, 'vendor_profile'):
        messages.error(request, 'You are not a registered vendor.')
        return redirect('marketplace:home')
    
    vendor = request.user.vendor_profile
    products = vendor.products.all()
    context = {'vendor': vendor, 'products': products}
    return render(request, 'marketplace/vendor_dashboard.html', context)


def input_list(request):
    """List all farming inputs"""
    inputs = Input.objects.filter(is_active=True)
    categories = InputCategory.objects.filter(is_active=True)
    context = {'inputs': inputs, 'categories': categories}
    return render(request, 'marketplace/inputs.html', context)


def input_detail(request, pk):
    """Input detail view"""
    input_item = get_object_or_404(Input, pk=pk, is_active=True)
    context = {'input_item': input_item}
    return render(request, 'marketplace/input_detail.html', context)


def input_category(request, pk):
    """Inputs by category"""
    category = get_object_or_404(InputCategory, pk=pk, is_active=True)
    inputs = category.inputs.filter(is_active=True)
    context = {'category': category, 'inputs': inputs}
    return render(request, 'marketplace/input_category.html', context)
