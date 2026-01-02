"""
Price analyzer - Statistical analysis of price data.
"""

from typing import List
from datetime import datetime, timedelta
import statistics
import numpy as np

from .models import PricePoint, PriceAnalysis, PriceTrend, Platform


class PriceAnalyzer:
    """Analyzes price data and trends"""
    
    def analyze_prices(self, price_history: List[PricePoint]) -> PriceAnalysis:
        """
        Analyze price history and generate statistics.
        
        Args:
            price_history: List of historical price points
            
        Returns:
            PriceAnalysis object with statistics
        """
        if not price_history:
            # Return default analysis if no history
            return PriceAnalysis(
                current_price=0.0,
                min_price=0.0,
                max_price=0.0,
                avg_price=0.0,
                median_price=0.0,
                trend=PriceTrend.STABLE,
                price_volatility=0.0,
                days_analyzed=0,
                price_history=[]
            )
        
        prices = [p.price for p in price_history]
        current_price = price_history[-1].price
        
        # Calculate statistics
        min_price = min(prices)
        max_price = max(prices)
        avg_price = statistics.mean(prices)
        median_price = statistics.median(prices)
        
        # Calculate volatility (standard deviation)
        volatility = statistics.stdev(prices) if len(prices) > 1 else 0.0
        
        # Determine trend
        trend = self._calculate_trend(prices)
        
        # Calculate days analyzed
        if len(price_history) > 1:
            days_analyzed = (price_history[-1].timestamp - price_history[0].timestamp).days
        else:
            days_analyzed = 0
        
        return PriceAnalysis(
            current_price=current_price,
            min_price=min_price,
            max_price=max_price,
            avg_price=avg_price,
            median_price=median_price,
            trend=trend,
            price_volatility=volatility,
            days_analyzed=days_analyzed,
            price_history=price_history
        )
    
    def _calculate_trend(self, prices: List[float]) -> PriceTrend:
        """
        Calculate price trend using linear regression.
        
        Args:
            prices: List of prices
            
        Returns:
            PriceTrend enum
        """
        if len(prices) < 3:
            return PriceTrend.STABLE
        
        # Simple linear regression
        x = np.arange(len(prices))
        y = np.array(prices)
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        
        # Calculate volatility
        volatility = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0
        
        # Determine trend
        if volatility > 0.15:  # 15% volatility threshold
            return PriceTrend.VOLATILE
        elif slope > np.mean(prices) * 0.01:  # Increasing by more than 1% per period
            return PriceTrend.INCREASING
        elif slope < -np.mean(prices) * 0.01:  # Decreasing by more than 1% per period
            return PriceTrend.DECREASING
        else:
            return PriceTrend.STABLE
    
    def compare_platforms(self, products: List) -> dict:
        """
        Compare prices across platforms.
        
        Args:
            products: List of Product objects
            
        Returns:
            Dictionary with comparison data
        """
        if not products:
            return {}
        
        comparison = {}
        for product in products:
            platform_name = product.platform.value
            comparison[platform_name] = {
                "price": product.current_price,
                "discount": product.discount_percentage,
                "rating": product.rating,
                "seller_trust": product.seller_info.get_trust_score() if product.seller_info else 0,
                "in_stock": product.in_stock
            }
        
        return comparison
    
    def calculate_savings(self, best_price: float, other_prices: List[float]) -> dict:
        """
        Calculate potential savings.
        
        Args:
            best_price: Best price found
            other_prices: Other prices for comparison
            
        Returns:
            Dictionary with savings information
        """
        if not other_prices:
            return {"amount": 0.0, "percentage": 0.0}
        
        max_price = max(other_prices)
        savings_amount = max_price - best_price
        savings_percentage = (savings_amount / max_price * 100) if max_price > 0 else 0.0
        
        return {
            "amount": round(savings_amount, 2),
            "percentage": round(savings_percentage, 2),
            "vs_highest": round(max_price, 2)
        }
