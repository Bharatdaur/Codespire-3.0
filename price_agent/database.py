"""
Database management for storing historical price data.
Uses SQLAlchemy for ORM and SQLite for storage.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from typing import List, Optional
import json

from .config import Config
from .models import Product, PricePoint, SellerInfo, Platform

Base = declarative_base()


class ProductDB(Base):
    """Product table"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True, index=True)
    name = Column(String)
    platform = Column(String)
    url = Column(String)
    image_url = Column(String)
    specifications = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class PriceHistoryDB(Base):
    """Price history table"""
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String, index=True)
    platform = Column(String)
    price = Column(Float)
    original_price = Column(Float, nullable=True)
    discount_percentage = Column(Float, default=0.0)
    is_sale = Column(Boolean, default=False)
    sale_name = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)


class SellerDB(Base):
    """Seller information table"""
    __tablename__ = "sellers"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String, index=True)
    platform = Column(String)
    name = Column(String)
    rating = Column(Float)
    total_ratings = Column(Integer)
    positive_percentage = Column(Float)
    is_verified = Column(Boolean, default=False)
    ship_on_time_percentage = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.now)


class DatabaseManager:
    """Manages database operations"""
    
    def __init__(self, db_url: str = None):
        """Initialize database connection"""
        self.db_url = db_url or Config.DATABASE_URL
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def save_product(self, product: Product) -> None:
        """Save or update product information"""
        session = self.get_session()
        try:
            existing = session.query(ProductDB).filter_by(product_id=product.product_id).first()
            
            if existing:
                existing.name = product.name
                existing.url = product.url
                existing.image_url = product.image_url
                existing.specifications = json.dumps(product.specifications)
                existing.updated_at = datetime.now()
            else:
                product_db = ProductDB(
                    product_id=product.product_id,
                    name=product.name,
                    platform=product.platform.value,
                    url=product.url,
                    image_url=product.image_url,
                    specifications=json.dumps(product.specifications)
                )
                session.add(product_db)
            
            session.commit()
        finally:
            session.close()
    
    def save_price(self, product_id: str, price_point: PricePoint) -> None:
        """Save price history"""
        session = self.get_session()
        try:
            price_db = PriceHistoryDB(
                product_id=product_id,
                platform=price_point.platform.value,
                price=price_point.price,
                original_price=price_point.original_price,
                discount_percentage=price_point.discount_percentage,
                is_sale=price_point.is_sale,
                sale_name=price_point.sale_name,
                timestamp=price_point.timestamp
            )
            session.add(price_db)
            session.commit()
        finally:
            session.close()
    
    def save_seller(self, product_id: str, seller_info: SellerInfo) -> None:
        """Save seller information"""
        session = self.get_session()
        try:
            seller_db = SellerDB(
                product_id=product_id,
                platform=seller_info.platform.value,
                name=seller_info.name,
                rating=seller_info.rating,
                total_ratings=seller_info.total_ratings,
                positive_percentage=seller_info.positive_percentage,
                is_verified=seller_info.is_verified,
                ship_on_time_percentage=seller_info.ship_on_time_percentage
            )
            session.add(seller_db)
            session.commit()
        finally:
            session.close()
    
    def get_price_history(
        self, 
        product_id: str, 
        platform: Platform, 
        days: int = 30
    ) -> List[PricePoint]:
        """Get price history for a product"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            prices = session.query(PriceHistoryDB).filter(
                PriceHistoryDB.product_id == product_id,
                PriceHistoryDB.platform == platform.value,
                PriceHistoryDB.timestamp >= cutoff_date
            ).order_by(PriceHistoryDB.timestamp.asc()).all()
            
            return [
                PricePoint(
                    price=p.price,
                    timestamp=p.timestamp,
                    platform=Platform(p.platform),
                    discount_percentage=p.discount_percentage,
                    original_price=p.original_price,
                    is_sale=p.is_sale,
                    sale_name=p.sale_name
                )
                for p in prices
            ]
        finally:
            session.close()
    
    def get_latest_seller(self, product_id: str, platform: Platform) -> Optional[SellerInfo]:
        """Get latest seller information"""
        session = self.get_session()
        try:
            seller = session.query(SellerDB).filter(
                SellerDB.product_id == product_id,
                SellerDB.platform == platform.value
            ).order_by(SellerDB.timestamp.desc()).first()
            
            if seller:
                return SellerInfo(
                    name=seller.name,
                    rating=seller.rating,
                    total_ratings=seller.total_ratings,
                    positive_percentage=seller.positive_percentage,
                    platform=Platform(seller.platform),
                    is_verified=seller.is_verified,
                    ship_on_time_percentage=seller.ship_on_time_percentage
                )
            return None
        finally:
            session.close()
    
    def cleanup_old_data(self, days: int = 90) -> None:
        """Remove price history older than specified days"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            session.query(PriceHistoryDB).filter(
                PriceHistoryDB.timestamp < cutoff_date
            ).delete()
            session.commit()
        finally:
            session.close()
