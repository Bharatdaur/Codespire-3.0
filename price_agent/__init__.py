"""
AI-Powered Price Comparison Agent

A sophisticated price comparison tool that leverages Gemini AI to analyze
product prices across Flipkart, Amazon, and Meesho, providing intelligent
recommendations and optimal purchase timing predictions.
"""

__version__ = "1.0.0"
__author__ = "Price Agent Team"

from .models import Product, PricePoint, SellerInfo, Recommendation

__all__ = [
    "Product",
    "PricePoint",
    "SellerInfo",
    "Recommendation",
]
