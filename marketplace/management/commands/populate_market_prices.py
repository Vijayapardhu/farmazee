"""
Management command to populate sample market price data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

# Crops functionality removed
from marketplace.models import MarketPrice


class Command(BaseCommand):
    help = 'Populate sample market price data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days of price history to create',
        )
        parser.add_argument(
            '--mandis',
            type=int,
            default=5,
            help='Number of mandis per crop',
        )

    def handle(self, *args, **options):
        self.stdout.write('Populating market price data...')
        
        days = options['days']
        mandis_per_crop = options['mandis']
        
        # Sample crops (crops functionality removed)
        crops = [
            {'name': 'Rice'},
            {'name': 'Wheat'},
            {'name': 'Cotton'},
            {'name': 'Tomato'},
            {'name': 'Maize'},
            {'name': 'Sugarcane'},
            {'name': 'Chilli'},
            {'name': 'Turmeric'},
            {'name': 'Groundnut'},
            {'name': 'Soybean'}
        ]
        
        # Sample mandis for Telangana/Andhra Pradesh
        mandis = [
            'Hyderabad APMC',
            'Warangal APMC', 
            'Karimnagar APMC',
            'Nizamabad APMC',
            'Guntur APMC',
            'Vijayawada APMC',
            'Kurnool APMC',
            'Tirupati APMC',
            'Rajahmundry APMC',
            'Vizag APMC'
        ]
        
        success_count = 0
        error_count = 0
        
        for crop in crops:
            self.stdout.write(f'Creating price data for {crop["name"]}...')
            
            # Select random mandis for this crop
            crop_mandis = random.sample(mandis, min(mandis_per_crop, len(mandis)))
            
            for mandi in crop_mandis:
                try:
                    # Base price varies by crop type
                    base_prices = {
                        'rice': 2150,
                        'wheat': 2200,
                        'maize': 1890,
                        'cotton': 6800,
                        'chilli': 8500,
                        'sugarcane': 320,
                        'tomato': 45,
                        'onion': 35,
                        'potato': 25,
                        'brinjal': 30,
                        'okra': 40,
                        'cabbage': 20,
                        'cauliflower': 25,
                        'spinach': 15,
                        'coriander': 50
                    }
                    
                    crop_key = crop["name"].lower()
                    base_price = base_prices.get(crop_key, 2000)  # Default price
                    
                    # Create price history for the last N days
                    for day_offset in range(days):
                        price_date = date.today() - timedelta(days=day_offset)
                        
                        # Skip if price already exists
                        if MarketPrice.objects.filter(
                            crop=crop, 
                            mandi_name=mandi, 
                            price_date=price_date
                        ).exists():
                            continue
                        
                        # Calculate price with some variation
                        variation = random.uniform(-0.15, 0.15)  # ±15% variation
                        current_price = base_price * (1 + variation)
                        
                        # Calculate change percentage (compared to previous day)
                        change_percentage = 0.0
                        if day_offset < days - 1:
                            previous_price = MarketPrice.objects.filter(
                                crop=crop,
                                mandi_name=mandi,
                                price_date=price_date + timedelta(days=1)
                            ).first()
                            
                            if previous_price:
                                change_percentage = ((current_price - float(previous_price.price_per_quintal)) / 
                                                   float(previous_price.price_per_quintal)) * 100
                        
                        # Random volume
                        volume = random.randint(50, 1000)
                        
                        # Mark current day's price as current
                        is_current = day_offset == 0
                        
                        MarketPrice.objects.create(
                            crop=crop,
                            mandi_name=mandi,
                            price_per_quintal=Decimal(str(round(current_price, 2))),
                            price_date=price_date,
                            change_percentage=round(change_percentage, 2),
                            volume=volume,
                            is_current=is_current
                        )
                        
                        success_count += 1
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating price for {crop["name"]} - {mandi}: {str(e)}')
                    )
                    error_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Market price data population completed!')
        self.stdout.write(f'Successfully created: {success_count} price records')
        if error_count > 0:
            self.stdout.write(f'Failed to create: {error_count} price records')
        
        # Show sample data
        self.stdout.write('\nSample current prices:')
        current_prices = MarketPrice.objects.filter(is_current=True)[:5]
        for price in current_prices:
            self.stdout.write(f'  {price.crop_name} - {price.mandi_name}: Rs.{price.price_per_quintal} ({price.price_change_display})')
        
        self.stdout.write('='*50)
