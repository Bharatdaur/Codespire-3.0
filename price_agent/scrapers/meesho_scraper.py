"""
Meesho scraper with mock data for demonstration.
In production, this would use web scraping with proper rate limiting.
"""

from typing import List, Optional
from datetime import datetime
import random
import hashlib

from .base_scraper import BaseScraper
from ..models import Product, SellerInfo, Platform


class MeeshoScraper(BaseScraper):
    """Meesho product scraper"""
    
    def get_platform(self) -> Platform:
        return Platform.MEESHO
    
    def search_product(self, query: str, max_results: int = 5) -> List[Product]:
        """
        Search for products on Meesho.
        Currently uses mock data for demonstration.
        """
        print(f"🔍 Searching Meesho for: {query}")
        
        # Generate mock products based on query
        # Meesho typically has lower prices
        products = []
        base_price = random.randint(3500, 35000)
        
        for i in range(min(max_results, 3)):
            product_id = self._generate_product_id(query, "meesho", i)
            price_variation = random.uniform(0.7, 1.1)
            current_price = base_price * price_variation
            original_price = current_price * random.uniform(1.2, 1.6)
            discount = self._calculate_discount(original_price, current_price)
            
            # Create seller info
            seller_info = SellerInfo(
                name=random.choice([
                    "Meesho Store",
                    "Value Bazaar",
                    "Budget Electronics",
                    "Smart Deals",
                    "Discount Hub"
                ]),
                rating=round(random.uniform(3.5, 4.5), 1),
                total_ratings=random.randint(100, 15000),
                positive_percentage=round(random.uniform(75, 92), 1),
                platform=Platform.MEESHO,
                is_verified=random.choice([True, False, False]),
                ship_on_time_percentage=round(random.uniform(80, 95), 1)
            )
            
            product = Product(
                name=f"{query} - Option {i+1}",
                product_id=product_id,
                platform=Platform.MEESHO,
                current_price=round(current_price, 2),
                original_price=round(original_price, 2),
                discount_percentage=discount,
                url=f"https://meesho.com/product/{product_id}",
                image_url=f"https://images.meesho.com/{product_id}.jpg",
                seller_info=seller_info,
                in_stock=random.choice([True, True, False]),
                rating=round(random.uniform(3.5, 4.4), 1),
                total_reviews=random.randint(50, 5000),
                specifications={
                    "Brand": random.choice(["Generic", "Local Brand", "Samsung", "Xiaomi", "Realme"]),
                    "Warranty": random.choice(["6 Months", "1 Year", "No Warranty"]),
                    "Color": random.choice(["Black", "White", "Blue", "Mixed"]),
                }
            )
            products.append(product)
        
        print(f"✅ Found {len(products)} products on Meesho")
        return products
    
    def get_product_details(self, product_url: str) -> Optional[Product]:
        """Get detailed product information"""
        # In production, this would scrape the product page
        # For now, return None as we use search_product
        return None
    
    def _generate_product_id(self, query: str, platform: str, index: int) -> str:
        """Generate consistent product ID based on query"""
        seed = f"{query}_{platform}_{index}"
        return hashlib.md5(seed.encode()).hexdigest()[:8].lower()
