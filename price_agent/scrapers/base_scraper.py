"""
Base scraper class defining the interface for all platform scrapers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import time
import random
import requests
from bs4 import BeautifulSoup

from ..models import Product, SellerInfo, Platform
from ..config import Config


class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.get_headers())
        self.delay = Config.REQUEST_DELAY
        self.max_retries = Config.MAX_RETRIES
        self.timeout = Config.TIMEOUT
    
    @abstractmethod
    def get_platform(self) -> Platform:
        """Return the platform this scraper handles"""
        pass
    
    @abstractmethod
    def search_product(self, query: str, max_results: int = 5) -> List[Product]:
        """
        Search for products by query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of Product objects
        """
        pass
    
    @abstractmethod
    def get_product_details(self, product_url: str) -> Optional[Product]:
        """
        Get detailed product information from URL.
        
        Args:
            product_url: Product page URL
            
        Returns:
            Product object or None if failed
        """
        pass
    
    def _make_request(self, url: str, method: str = "GET", **kwargs) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic.
        
        Args:
            url: URL to request
            method: HTTP method
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                # Add random delay to avoid detection
                time.sleep(self.delay + random.uniform(0, 1))
                
                if method.upper() == "GET":
                    response = self.session.get(url, timeout=self.timeout, **kwargs)
                elif method.upper() == "POST":
                    response = self.session.post(url, timeout=self.timeout, **kwargs)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response
                
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    print(f"❌ Failed to fetch {url} after {self.max_retries} attempts: {e}")
                    return None
                
                # Exponential backoff
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
        
        return None
    
    def _parse_html(self, html: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content.
        
        Args:
            html: HTML string
            
        Returns:
            BeautifulSoup object or None
        """
        try:
            return BeautifulSoup(html, 'lxml')
        except Exception as e:
            print(f"❌ Failed to parse HTML: {e}")
            return None
    
    def _extract_price(self, price_str: str) -> float:
        """
        Extract numeric price from string.
        
        Args:
            price_str: Price string (e.g., "₹1,299.00", "$99.99")
            
        Returns:
            Float price value
        """
        try:
            # Remove currency symbols and commas
            cleaned = price_str.replace('₹', '').replace('$', '').replace(',', '').strip()
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0.0
    
    def _calculate_discount(self, original_price: float, current_price: float) -> float:
        """
        Calculate discount percentage.
        
        Args:
            original_price: Original price
            current_price: Current price
            
        Returns:
            Discount percentage
        """
        if original_price > 0 and current_price < original_price:
            return round(((original_price - current_price) / original_price) * 100, 2)
        return 0.0
    
    def close(self):
        """Close the session"""
        self.session.close()
