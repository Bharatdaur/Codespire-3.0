"""
Price predictor - Statistical prediction of future prices and optimal buy timing.
"""

from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from .models import PricePoint, PricePrediction
from .config import Config


class PricePredictor:
    """Predicts future prices and optimal purchase timing"""
    
    def predict_price(
        self, 
        price_history: List[PricePoint],
        days_ahead: int = 7
    ) -> PricePrediction:
        """
        Predict future price and optimal buy timing.
        
        Args:
            price_history: Historical price data
            days_ahead: Number of days to predict ahead
            
        Returns:
            PricePrediction object
        """
        if len(price_history) < 7:
            # Not enough data for prediction
            return self._default_prediction(price_history)
        
        # Extract prices and dates
        prices = [p.price for p in price_history]
        current_price = prices[-1]
        
        # Simple prediction using moving average and trend
        predicted_price = self._simple_forecast(prices, days_ahead)
        
        # Calculate confidence based on data quality
        confidence = self._calculate_confidence(prices)
        
        # Check for upcoming sales
        upcoming_sale, days_until_sale = self._check_upcoming_sales()
        
        # Calculate expected price drop
        expected_drop = max(0, current_price - predicted_price)
        expected_drop_percent = (expected_drop / current_price * 100) if current_price > 0 else 0
        
        # Determine optimal buy date
        optimal_date = None
        if upcoming_sale and days_until_sale and days_until_sale <= 30:
            optimal_date = datetime.now() + timedelta(days=days_until_sale)
        elif expected_drop_percent > 5:
            optimal_date = datetime.now() + timedelta(days=days_ahead)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            current_price,
            predicted_price,
            upcoming_sale,
            days_until_sale
        )
        
        return PricePrediction(
            predicted_price=round(predicted_price, 2),
            confidence=round(confidence, 2),
            optimal_buy_date=optimal_date,
            expected_price_drop=round(expected_drop, 2),
            upcoming_sale=upcoming_sale,
            days_until_sale=days_until_sale,
            recommendation=recommendation
        )
    
    def _simple_forecast(self, prices: List[float], days_ahead: int) -> float:
        """
        Simple forecasting using exponential smoothing.
        
        Args:
            prices: Historical prices
            days_ahead: Days to forecast
            
        Returns:
            Predicted price
        """
        try:
            # Use exponential smoothing for prediction
            if len(prices) >= 10:
                model = ExponentialSmoothing(
                    prices,
                    seasonal_periods=7,
                    trend='add',
                    seasonal='add'
                )
                fitted = model.fit()
                forecast = fitted.forecast(steps=days_ahead)
                return float(forecast[-1])
            else:
                # Simple moving average for small datasets
                recent_prices = prices[-7:]
                return np.mean(recent_prices)
        except:
            # Fallback to simple average
            return np.mean(prices[-7:])
    
    def _calculate_confidence(self, prices: List[float]) -> float:
        """
        Calculate prediction confidence based on data quality.
        
        Args:
            prices: Historical prices
            
        Returns:
            Confidence score (0-100)
        """
        # Base confidence on data points
        data_confidence = min(len(prices) / 30 * 50, 50)
        
        # Reduce confidence for high volatility
        volatility = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 1
        volatility_penalty = min(volatility * 50, 30)
        
        confidence = data_confidence + (50 - volatility_penalty)
        return max(30, min(95, confidence))
    
    def _check_upcoming_sales(self) -> tuple[Optional[str], Optional[int]]:
        """
        Check for upcoming sale events.
        
        Returns:
            Tuple of (sale_name, days_until_sale)
        """
        today = datetime.now()
        current_month = today.month
        current_day = today.day
        
        # Check sale events from config
        upcoming_sales = []
        
        for sale_name, sale_info in Config.SALE_EVENTS.items():
            sale_month = sale_info["month"]
            sale_days = sale_info["days"]
            
            for sale_day in sale_days:
                # Calculate sale date
                if sale_month >= current_month:
                    sale_date = datetime(today.year, sale_month, sale_day)
                else:
                    sale_date = datetime(today.year + 1, sale_month, sale_day)
                
                days_until = (sale_date - today).days
                
                if 0 <= days_until <= 60:  # Within next 60 days
                    upcoming_sales.append((sale_name, days_until))
        
        if upcoming_sales:
            # Return the nearest sale
            upcoming_sales.sort(key=lambda x: x[1])
            return upcoming_sales[0]
        
        return None, None
    
    def _generate_recommendation(
        self,
        current_price: float,
        predicted_price: float,
        upcoming_sale: Optional[str],
        days_until_sale: Optional[int]
    ) -> str:
        """Generate buy/wait recommendation"""
        price_change_percent = ((predicted_price - current_price) / current_price * 100) if current_price > 0 else 0
        
        if upcoming_sale and days_until_sale and days_until_sale <= 14:
            return f"WAIT - {upcoming_sale} in {days_until_sale} days"
        elif price_change_percent < -5:
            return "WAIT - Price expected to drop"
        elif price_change_percent > 5:
            return "BUY NOW - Price expected to increase"
        else:
            return "BUY NOW - Good time to purchase"
    
    def _default_prediction(self, price_history: List[PricePoint]) -> PricePrediction:
        """Return default prediction when insufficient data"""
        current_price = price_history[-1].price if price_history else 0.0
        upcoming_sale, days_until_sale = self._check_upcoming_sales()
        
        recommendation = "BUY NOW - Insufficient data for prediction"
        if upcoming_sale and days_until_sale and days_until_sale <= 14:
            recommendation = f"WAIT - {upcoming_sale} in {days_until_sale} days"
        
        return PricePrediction(
            predicted_price=current_price,
            confidence=30.0,
            upcoming_sale=upcoming_sale,
            days_until_sale=days_until_sale,
            recommendation=recommendation
        )
