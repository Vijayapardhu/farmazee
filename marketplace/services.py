"""
Marketplace Services for Farmazee
Handles market prices, product management, and order processing
"""

import requests
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.cache import cache
from django.conf import settings
from .models import Product, MarketPrice, Order, Vendor

logger = logging.getLogger(__name__)


class MarketPriceService:
    """Service for managing market prices and price data"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'MARKET_API_URL', 'https://api.example.com')
        self.api_key = getattr(settings, 'MARKET_API_KEY', None)
        self.cache_duration = 1800  # 30 minutes
    
    def get_live_prices(self, crop_name=None, mandi_name=None, limit=10):
        """Get live market prices from API or database"""
        cache_key = f'market_prices_{crop_name}_{mandi_name}_{limit}'
        
        # Check cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        try:
            # Try to get from external API first
            if self.api_key and crop_name:
                prices = self._fetch_from_api(crop_name, mandi_name)
            else:
                # Fallback to database
                prices = self._fetch_from_database(crop_name, mandi_name, limit)
            
            # Cache the results
            cache.set(cache_key, prices, self.cache_duration)
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching market prices: {e}")
            # Return fallback data
            return self._get_fallback_prices(crop_name)
    
    def _fetch_from_api(self, crop_name, mandi_name):
        """Fetch prices from external API (eNAM or similar)"""
        # This would integrate with real market APIs
        # For now, return structured data
        return {
            'crop': crop_name,
            'prices': [
                {
                    'mandi_name': 'Hyderabad APMC',
                    'price_per_quintal': 2150,
                    'change_percentage': 2.5,
                    'volume': 500,
                    'last_updated': datetime.now().isoformat()
                }
            ]
        }
    
    def _fetch_from_database(self, crop_name, mandi_name, limit):
        """Fetch prices from local database"""
        queryset = MarketPrice.objects.select_related('crop').order_by('-price_date')
        
        if crop_name:
            queryset = queryset.filter(crop__name__icontains=crop_name)
        if mandi_name:
            queryset = queryset.filter(mandi_name__icontains=mandi_name)
        
        prices = queryset[:limit]
        
        return {
            'crop': crop_name or 'All Crops',
            'prices': [
                {
                    'mandi_name': price.mandi_name,
                    'price_per_quintal': float(price.price_per_quintal),
                    'change_percentage': price.change_percentage,
                    'volume': price.volume,
                    'last_updated': price.price_date.isoformat()
                }
                for price in prices
            ]
        }
    
    def _get_fallback_prices(self, crop_name):
        """Get fallback prices when API/database fails"""
        fallback_data = {
            'rice': {'price': 2150, 'change': 2.5},
            'cotton': {'price': 6800, 'change': 1.8},
            'maize': {'price': 1890, 'change': -1.2},
            'chilli': {'price': 8500, 'change': 5.2},
            'wheat': {'price': 2200, 'change': 0.8},
            'sugarcane': {'price': 320, 'change': 1.5},
        }
        
        crop_key = crop_name.lower() if crop_name else 'rice'
        data = fallback_data.get(crop_key, fallback_data['rice'])
        
        return {
            'crop': crop_name or 'Rice',
            'prices': [
                {
                    'mandi_name': 'Hyderabad APMC',
                    'price_per_quintal': data['price'],
                    'change_percentage': data['change'],
                    'volume': 500,
                    'last_updated': datetime.now().isoformat()
                }
            ]
        }
    
    def update_price(self, crop_name, mandi_name, price, volume=None):
        """Update market price in database"""
        try:
            # Get previous price for change calculation
            previous_price = MarketPrice.objects.filter(
                crop_name__iexact=crop_name, mandi_name=mandi_name
            ).order_by('-price_date').first()
            
            change_percentage = 0
            if previous_price:
                change_percentage = ((price - previous_price.price_per_quintal) / 
                                   previous_price.price_per_quintal) * 100
            
            # Create new price record
            MarketPrice.objects.create(
                crop_name=crop_name,
                mandi_name=mandi_name,
                price_per_quintal=price,
                price_date=datetime.now().date(),
                change_percentage=change_percentage,
                volume=volume or 0
            )
            
            # Clear cache
            cache.delete_many([
                f'market_prices_{crop_name}_',
                f'market_prices_None_',
                'market_prices_all'
            ])
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating price: {e}")
            return False
    
    def get_price_trends(self, crop_name, days=30):
        """Get price trends for a crop over time"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            prices = MarketPrice.objects.filter(
                crop_name__iexact=crop_name,
                price_date__range=[start_date, end_date]
            ).order_by('price_date')
            
            return [
                {
                    'date': price.price_date.isoformat(),
                    'price': float(price.price_per_quintal),
                    'volume': price.volume
                }
                for price in prices
            ]
            
        except Exception as e:
            logger.error(f"Error getting price trends: {e}")
            return []
    
    def get_price_alerts(self, threshold_percentage=5):
        """Get price alerts for significant changes"""
        from django.db.models import F, Q
        
        alerts = MarketPrice.objects.filter(
            Q(change_percentage__gte=threshold_percentage) |
            Q(change_percentage__lte=-threshold_percentage),
            price_date=datetime.now().date()
        ).select_related('crop')
        
        return [
            {
                'crop': price.crop.name,
                'mandi': price.mandi_name,
                'price': float(price.price_per_quintal),
                'change': price.change_percentage,
                'type': 'increase' if price.change_percentage > 0 else 'decrease'
            }
            for price in alerts
        ]


class ProductService:
    """Service for managing marketplace products"""
    
    def get_featured_products(self, limit=8):
        """Get featured products"""
        return Product.objects.filter(
            is_featured=True,
            is_active=True
        ).select_related('category', 'vendor')[:limit]
    
    def search_products(self, query, category=None, min_price=None, max_price=None):
        """Search products with filters"""
        queryset = Product.objects.filter(
            is_active=True
        ).select_related('category', 'vendor')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.order_by('-created_at')
    
    def get_product_recommendations(self, user, limit=5):
        """Get personalized product recommendations"""
        # Simple recommendation based on common farming needs
        try:
            return Product.objects.filter(
                category__name__in=['Seeds', 'Fertilizers', 'Pesticides'],
                is_active=True
            ).select_related('category', 'vendor')[:limit]
        except:
            pass
        
        # Fallback to featured products
        return self.get_featured_products(limit)


class OrderService:
    """Service for managing orders"""
    
    def create_order(self, user, items, shipping_address):
        """Create a new order"""
        try:
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                status='pending'
            )
            
            total_amount = 0
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                
                order_item = order.items.create(
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                total_amount += product.price * quantity
            
            order.total_amount = total_amount
            order.save()
            
            return order
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
    
    def get_user_orders(self, user):
        """Get all orders for a user"""
        return Order.objects.filter(user=user).order_by('-created_at')
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return True
        except Order.DoesNotExist:
            return False


# Initialize services
market_price_service = MarketPriceService()
product_service = ProductService()
order_service = OrderService()
