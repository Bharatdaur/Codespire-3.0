"""
Data models for the Price Comparison Agent.
Defines the structure for products, prices, sellers, and recommendations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum


class Platform(Enum):
    """E-commerce platforms"""
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MEESHO = "meesho"


class PriceTrend(Enum):
    """Price trend indicators"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


@dataclass
class SellerInfo:
    """Seller information and ratings"""
    name: str
    rating: float  # 0-5 scale
    total_ratings: int
    positive_percentage: float  # 0-100
    platform: Platform
    is_verified: bool = False
    ship_on_time_percentage: float = 0.0
    
    def get_trust_score(self) -> float:
        """Calculate overall trust score (0-100)"""
        score = 0.0
        score += (self.rating / 5.0) * 40  # Rating contributes 40%
        score += (self.positive_percentage / 100.0) * 30  # Positive reviews 30%
        score += (self.ship_on_time_percentage / 100.0) * 20  # Shipping 20%
        score += 10 if self.is_verified else 0  # Verification 10%
        return round(score, 2)


@dataclass
class PricePoint:
    """Historical price data point"""
    price: float
    timestamp: datetime
    platform: Platform
    discount_percentage: float = 0.0
    original_price: Optional[float] = None
    is_sale: bool = False
    sale_name: Optional[str] = None
    
    def get_effective_price(self) -> float:
        """Get the actual price after discount"""
        return self.price


@dataclass
class Product:
    """Product information"""
    name: str
    product_id: str
    platform: Platform
    current_price: float
    original_price: Optional[float] = None
    discount_percentage: float = 0.0
    url: str = ""
    image_url: str = ""
    seller_info: Optional[SellerInfo] = None
    in_stock: bool = True
    rating: float = 0.0
    total_reviews: int = 0
    specifications: Dict[str, str] = field(default_factory=dict)
    
    def get_final_price(self) -> float:
        """Get final price after discount"""
        return self.current_price
    
    def get_savings(self) -> float:
        """Calculate savings amount"""
        if self.original_price:
            return self.original_price - self.current_price
        return 0.0


@dataclass
class PriceAnalysis:
    """Price analysis results"""
    current_price: float
    min_price: float
    max_price: float
    avg_price: float
    median_price: float
    trend: PriceTrend
    price_volatility: float  # Standard deviation
    days_analyzed: int
    price_history: List[PricePoint] = field(default_factory=list)
    
    def get_price_position(self) -> str:
        """Determine if current price is good, average, or high"""
        if self.current_price <= self.min_price * 1.05:
            return "excellent"
        elif self.current_price <= self.avg_price * 0.95:
            return "good"
        elif self.current_price <= self.avg_price * 1.05:
            return "average"
        else:
            return "high"


@dataclass
class PricePrediction:
    """Price prediction results"""
    predicted_price: float
    confidence: float  # 0-100
    optimal_buy_date: Optional[datetime] = None
    expected_price_drop: float = 0.0
    upcoming_sale: Optional[str] = None
    days_until_sale: Optional[int] = None
    recommendation: str = ""
    
    def should_buy_now(self) -> bool:
        """Determine if it's a good time to buy now"""
        return self.expected_price_drop < 5.0 or self.confidence < 60


@dataclass
class Recommendation:
    """Final recommendation for the user"""
    best_platform: Platform
    best_price: float
    best_product: Product
    all_products: List[Product] = field(default_factory=list)
    price_analysis: Optional[PriceAnalysis] = None
    prediction: Optional[PricePrediction] = None
    
    # AI-generated insights
    summary: str = ""
    detailed_analysis: str = ""
    timing_advice: str = ""
    alternative_suggestions: List[str] = field(default_factory=list)
    
    # Savings information
    total_savings: float = 0.0
    savings_percentage: float = 0.0
    
    def get_price_comparison(self) -> Dict[str, float]:
        """Get price comparison across platforms"""
        comparison = {}
        for product in self.all_products:
            comparison[product.platform.value] = product.current_price
        return comparison
    
    def get_best_seller_score(self) -> float:
        """Get trust score of best seller"""
        if self.best_product.seller_info:
            return self.best_product.seller_info.get_trust_score()
        return 0.0
