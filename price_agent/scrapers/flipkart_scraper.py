"""
Flipkart scraper with mock data for demonstration.
In production, this would use Flipkart Affiliate API or web scraping.
"""

from typing import List, Optional
from datetime import datetime
import random
import hashlib

from .base_scraper import BaseScraper
from ..models import Product, SellerInfo, Platform


class FlipkartScraper(BaseScraper):
    """Flipkart product scraper"""
    
    def get_platform(self) -> Platform:
        return Platform.FLIPKART
    
    def search_product(self, query: str, max_results: int = 5) -> List[Product]:
        """
        Search for products on Flipkart.
        Currently uses mock data for demonstration.
        """
        print(f"🔍 Searching Flipkart for: {query}")
        
        # Generate mock products based on query
        products = []
        base_price = random.randint(4800, 48000)  # Slightly different pricing
        
        for i in range(min(max_results, 3)):
            product_id = self._generate_product_id(query, "flipkart", i)
            price_variation = random.uniform(0.85, 1.15)
            current_price = base_price * price_variation
            original_price = current_price * random.uniform(1.15, 1.5)
            discount = self._calculate_discount(original_price, current_price)
            
            # Create seller info
            seller_info = SellerInfo(
                name=random.choice([
                    "Flipkart",
                    "RetailNet",
                    "Omnitech Retail",
                    "SuperComNet",
                    "TechZone India"
                ]),
                rating=round(random.uniform(3.9, 4.7), 1),
                total_ratings=random.randint(300, 40000),
                positive_percentage=round(random.uniform(82, 96), 1),
                platform=Platform.FLIPKART,
                is_verified=random.choice([True, True, False]),
                ship_on_time_percentage=round(random.uniform(88, 97), 1)
            )
            
            product = Product(
                name=f"{query} - Variant {chr(88+i)}",
                product_id=product_id,
                platform=Platform.FLIPKART,
                current_price=round(current_price, 2),
                original_price=round(original_price, 2),
                discount_percentage=discount,
                url=f"https://flipkart.com/product/{product_id}",
                image_url=f"https://rukminim2.flixcart.com/{product_id}.jpg",
                seller_info=seller_info,
                in_stock=random.choice([True, True, True, False]),
                rating=round(random.uniform(3.7, 4.6), 1),
                total_reviews=random.randint(80, 8000),
                specifications={
                    "Brand": random.choice(["Samsung", "Dell", "HP", "Asus", "Acer"]),
                    "Warranty": random.choice(["1 Year", "2 Years", "3 Years"]),
                    "Color": random.choice(["Black", "Grey", "Blue", "Red"]),
                }
            )
            products.append(product)
        
        print(f"✅ Found {len(products)} products on Flipkart")
        return products
    
    def get_product_details(self, product_url: str) -> Optional[Product]:
        """Get detailed product information"""
        # In production, this would scrape the product page
        # For now, return None as we use search_product
        return None
    
    def _generate_product_id(self, query: str, platform: str, index: int) -> str:
        """Generate consistent product ID based on query"""
        seed = f"{query}_{platform}_{index}"
        return hashlib.md5(seed.encode()).hexdigest()[:12].upper()
