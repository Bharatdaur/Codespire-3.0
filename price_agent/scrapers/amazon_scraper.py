"""
Amazon scraper with mock data for demonstration.
In production, this would integrate with Amazon Product Advertising API or web scraping.
"""

from typing import List, Optional
from datetime import datetime
import random
import hashlib

from .base_scraper import BaseScraper
from ..models import Product, SellerInfo, Platform


class AmazonScraper(BaseScraper):
    """Amazon product scraper"""
    
    def get_platform(self) -> Platform:
        return Platform.AMAZON
    
    def search_product(self, query: str, max_results: int = 5) -> List[Product]:
        """
        Search for products on Amazon.
        Currently uses mock data for demonstration.
        """
        print(f"🔍 Searching Amazon for: {query}")
        
        # Generate mock products based on query
        products = []
        base_price = random.randint(5000, 50000)
        
        for i in range(min(max_results, 3)):
            product_id = self._generate_product_id(query, "amazon", i)
            price_variation = random.uniform(0.8, 1.2)
            current_price = base_price * price_variation
            original_price = current_price * random.uniform(1.1, 1.4)
            discount = self._calculate_discount(original_price, current_price)
            
            # Create seller info
            seller_info = SellerInfo(
                name=random.choice([
                    "Amazon.in",
                    "Cloudtail India",
                    "Appario Retail",
                    "RetailNet",
                    "TechMart India"
                ]),
                rating=round(random.uniform(4.0, 4.8), 1),
                total_ratings=random.randint(500, 50000),
                positive_percentage=round(random.uniform(85, 98), 1),
                platform=Platform.AMAZON,
                is_verified=random.choice([True, True, False]),
                ship_on_time_percentage=round(random.uniform(90, 99), 1)
            )
            
            product = Product(
                name=f"{query} - Model {chr(65+i)}",
                product_id=product_id,
                platform=Platform.AMAZON,
                current_price=round(current_price, 2),
                original_price=round(original_price, 2),
                discount_percentage=discount,
                url=f"https://amazon.in/dp/{product_id}",
                image_url=f"https://m.media-amazon.com/images/{product_id}.jpg",
                seller_info=seller_info,
                in_stock=random.choice([True, True, True, False]),
                rating=round(random.uniform(3.8, 4.7), 1),
                total_reviews=random.randint(100, 10000),
                specifications={
                    "Brand": random.choice(["Samsung", "Dell", "HP", "Lenovo", "Apple"]),
                    "Warranty": random.choice(["1 Year", "2 Years", "3 Years"]),
                    "Color": random.choice(["Black", "Silver", "Blue", "White"]),
                }
            )
            products.append(product)
        
        print(f"✅ Found {len(products)} products on Amazon")
        return products
    
    def get_product_details(self, product_url: str) -> Optional[Product]:
        """Get detailed product information"""
        # In production, this would scrape the product page
        # For now, return None as we use search_product
        return None
    
    def _generate_product_id(self, query: str, platform: str, index: int) -> str:
        """Generate consistent product ID based on query"""
        seed = f"{query}_{platform}_{index}"
        return hashlib.md5(seed.encode()).hexdigest()[:10].upper()
