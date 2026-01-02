"""
Gemini AI Agent - Core intelligence engine for price analysis and recommendations.
"""

from google import genai
from google.genai import types
from typing import List, Dict, Optional
import json
import os

from .models import Product, PriceAnalysis, PricePrediction, Platform
from .config import Config


class GeminiAgent:
    """Gemini AI-powered analysis and recommendation engine"""
    
    def __init__(self):
        """Initialize Gemini AI"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        # Initialize client with API key
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = Config.GEMINI_MODEL
        self.temperature = Config.GEMINI_TEMPERATURE
    
    def analyze_products(
        self,
        products: List[Product],
        price_analysis: Optional[PriceAnalysis] = None,
        prediction: Optional[PricePrediction] = None
    ) -> Dict[str, str]:
        """
        Use Gemini AI to analyze products and generate insights.
        
        Args:
            products: List of products from different platforms
            price_analysis: Statistical price analysis
            prediction: Price prediction data
            
        Returns:
            Dictionary with AI-generated insights
        """
        # Prepare data for Gemini
        product_data = self._prepare_product_data(products)
        analysis_data = self._prepare_analysis_data(price_analysis)
        prediction_data = self._prepare_prediction_data(prediction)
        
        # Create comprehensive prompt
        prompt = self._create_analysis_prompt(product_data, analysis_data, prediction_data)
        
        try:
            # Generate AI analysis using new API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                )
            )
            
            # Parse response
            insights = self._parse_ai_response(response.text)
            return insights
            
        except Exception as e:
            print(f"⚠️  Gemini AI error: {e}")
            return self._fallback_analysis(products)
    
    def _prepare_product_data(self, products: List[Product]) -> str:
        """Prepare product data for AI analysis"""
        data = []
        for p in products:
            seller_trust = p.seller_info.get_trust_score() if p.seller_info else 0
            data.append({
                "platform": p.platform.value,
                "name": p.name,
                "price": p.current_price,
                "original_price": p.original_price,
                "discount": f"{p.discount_percentage}%",
                "rating": p.rating,
                "reviews": p.total_reviews,
                "seller": p.seller_info.name if p.seller_info else "Unknown",
                "seller_trust_score": f"{seller_trust}/100",
                "in_stock": p.in_stock
            })
        return json.dumps(data, indent=2)
    
    def _prepare_analysis_data(self, analysis: Optional[PriceAnalysis]) -> str:
        """Prepare price analysis data"""
        if not analysis:
            return "No historical data available"
        
        return json.dumps({
            "current_price": analysis.current_price,
            "min_price": analysis.min_price,
            "max_price": analysis.max_price,
            "average_price": analysis.avg_price,
            "trend": analysis.trend.value,
            "price_position": analysis.get_price_position(),
            "days_analyzed": analysis.days_analyzed
        }, indent=2)
    
    def _prepare_prediction_data(self, prediction: Optional[PricePrediction]) -> str:
        """Prepare prediction data"""
        if not prediction:
            return "No prediction available"
        
        return json.dumps({
            "predicted_price": prediction.predicted_price,
            "confidence": f"{prediction.confidence}%",
            "expected_drop": prediction.expected_price_drop,
            "upcoming_sale": prediction.upcoming_sale,
            "days_until_sale": prediction.days_until_sale,
            "recommendation": prediction.recommendation
        }, indent=2)
    
    def _create_analysis_prompt(
        self,
        product_data: str,
        analysis_data: str,
        prediction_data: str
    ) -> str:
        """Create comprehensive prompt for Gemini"""
        return f"""You are an expert e-commerce price analyst helping users make smart purchasing decisions.

**PRODUCTS COMPARISON:**
{product_data}

**PRICE ANALYSIS:**
{analysis_data}

**PRICE PREDICTION:**
{prediction_data}

Please provide a comprehensive analysis in the following JSON format:
{{
    "summary": "A concise 2-3 sentence summary highlighting the best deal and key insight",
    "detailed_analysis": "Detailed comparison of prices, discounts, and seller trustworthiness across platforms. Explain which platform offers the best value and why.",
    "timing_advice": "Clear advice on when to buy - should they buy now or wait? Explain the reasoning based on price trends and upcoming sales.",
    "alternative_suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
}}

**Guidelines:**
1. Be specific with numbers (prices, discounts, savings)
2. Consider both price AND seller trustworthiness
3. Make actionable recommendations
4. Explain the reasoning clearly
5. Keep it user-friendly and conversational
6. If there's an upcoming sale, strongly emphasize it
7. Highlight the best overall value (not just lowest price)

Provide ONLY the JSON response, no additional text."""
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, str]:
        """Parse AI response into structured format"""
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                parsed = json.loads(json_str)
                return parsed
            else:
                # Fallback: use entire response as summary
                return {
                    "summary": response_text[:200],
                    "detailed_analysis": response_text,
                    "timing_advice": "Please review the analysis above.",
                    "alternative_suggestions": []
                }
        except json.JSONDecodeError:
            return {
                "summary": response_text[:200],
                "detailed_analysis": response_text,
                "timing_advice": "Please review the analysis above.",
                "alternative_suggestions": []
            }
    
    def _fallback_analysis(self, products: List[Product]) -> Dict[str, str]:
        """Fallback analysis if AI fails"""
        if not products:
            return {
                "summary": "No products found for comparison.",
                "detailed_analysis": "Unable to perform analysis.",
                "timing_advice": "Please try a different search query.",
                "alternative_suggestions": []
            }
        
        # Find best price
        best_product = min(products, key=lambda p: p.current_price)
        
        return {
            "summary": f"Best price found on {best_product.platform.value} at ₹{best_product.current_price:.2f}",
            "detailed_analysis": f"Comparing {len(products)} products across platforms. {best_product.platform.value} offers the lowest price.",
            "timing_advice": "Consider purchasing now if the price meets your budget.",
            "alternative_suggestions": [
                "Check seller ratings before purchasing",
                "Compare shipping costs",
                "Look for additional coupons"
            ]
        }
