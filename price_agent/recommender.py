"""
Recommendation engine - Combines all analysis to generate final recommendations.
"""

from typing import List
from datetime import datetime

from .models import Product, Recommendation, PriceAnalysis, PricePrediction, Platform
from .analyzer import PriceAnalyzer
from .predictor import PricePredictor
from .gemini_agent import GeminiAgent
from .database import DatabaseManager


class Recommender:
    """Generates comprehensive product recommendations"""
    
    def __init__(self):
        self.analyzer = PriceAnalyzer()
        self.predictor = PricePredictor()
        self.gemini = GeminiAgent()
        self.db = DatabaseManager()
    
    def generate_recommendation(
        self,
        products: List[Product],
        query: str
    ) -> Recommendation:
        """
        Generate comprehensive recommendation.
        
        Args:
            products: List of products from all platforms
            query: Original search query
            
        Returns:
            Recommendation object with AI insights
        """
        if not products:
            return self._empty_recommendation()
        
        # Find best product (considering price and trust)
        best_product = self._find_best_product(products)
        
        # Get price history and analysis
        price_history = self._get_price_history(best_product)
        price_analysis = self.analyzer.analyze_prices(price_history) if price_history else None
        
        # Get price prediction
        prediction = self.predictor.predict_price(price_history) if price_history else None
        
        # Calculate savings
        all_prices = [p.current_price for p in products if p.in_stock]
        savings_info = self.analyzer.calculate_savings(best_product.current_price, all_prices)
        
        # Get AI-powered insights
        ai_insights = self.gemini.analyze_products(products, price_analysis, prediction)
        
        # Create recommendation
        recommendation = Recommendation(
            best_platform=best_product.platform,
            best_price=best_product.current_price,
            best_product=best_product,
            all_products=products,
            price_analysis=price_analysis,
            prediction=prediction,
            summary=ai_insights.get("summary", ""),
            detailed_analysis=ai_insights.get("detailed_analysis", ""),
            timing_advice=ai_insights.get("timing_advice", ""),
            alternative_suggestions=ai_insights.get("alternative_suggestions", []),
            total_savings=savings_info.get("amount", 0.0),
            savings_percentage=savings_info.get("percentage", 0.0)
        )
        
        # Save to database
        self._save_to_database(products, price_history)
        
        return recommendation
    
    def _find_best_product(self, products: List[Product]) -> Product:
        """
        Find best product considering price, availability, and seller trust.
        
        Args:
            products: List of products
            
        Returns:
            Best product
        """
        # Filter in-stock products
        in_stock = [p for p in products if p.in_stock]
        
        if not in_stock:
            # Return cheapest even if out of stock
            return min(products, key=lambda p: p.current_price)
        
        # Score each product
        scored_products = []
        for product in in_stock:
            # Calculate composite score
            price_score = 100 - (product.current_price / max(p.current_price for p in in_stock) * 100)
            trust_score = product.seller_info.get_trust_score() if product.seller_info else 50
            rating_score = (product.rating / 5.0) * 100
            
            # Weighted score: 50% price, 30% trust, 20% rating
            total_score = (price_score * 0.5) + (trust_score * 0.3) + (rating_score * 0.2)
            
            scored_products.append((product, total_score))
        
        # Return product with highest score
        best = max(scored_products, key=lambda x: x[1])
        return best[0]
    
    def _get_price_history(self, product: Product) -> List:
        """Get price history from database"""
        try:
            return self.db.get_price_history(
                product.product_id,
                product.platform,
                days=30
            )
        except:
            return []
    
    def _save_to_database(self, products: List[Product], price_history: List):
        """Save products and prices to database"""
        try:
            for product in products:
                # Save product
                self.db.save_product(product)
                
                # Save current price
                from .models import PricePoint
                price_point = PricePoint(
                    price=product.current_price,
                    timestamp=datetime.now(),
                    platform=product.platform,
                    discount_percentage=product.discount_percentage,
                    original_price=product.original_price
                )
                self.db.save_price(product.product_id, price_point)
                
                # Save seller info
                if product.seller_info:
                    self.db.save_seller(product.product_id, product.seller_info)
        except Exception as e:
            print(f"⚠️  Database save error: {e}")
    
    def _empty_recommendation(self) -> Recommendation:
        """Return empty recommendation when no products found"""
        from .models import Product, Platform
        
        empty_product = Product(
            name="No products found",
            product_id="",
            platform=Platform.AMAZON,
            current_price=0.0
        )
        
        return Recommendation(
            best_platform=Platform.AMAZON,
            best_price=0.0,
            best_product=empty_product,
            all_products=[],
            summary="No products found for your search query.",
            detailed_analysis="Please try a different search term.",
            timing_advice="",
            alternative_suggestions=[]
        )
