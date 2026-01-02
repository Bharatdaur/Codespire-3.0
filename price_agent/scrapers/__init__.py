"""
Scrapers package for platform-specific data collection.
"""

from .base_scraper import BaseScraper
from .amazon_scraper import AmazonScraper
from .flipkart_scraper import FlipkartScraper
from .meesho_scraper import MeeshoScraper

__all__ = [
    "BaseScraper",
    "AmazonScraper",
    "FlipkartScraper",
    "MeeshoScraper",
]
