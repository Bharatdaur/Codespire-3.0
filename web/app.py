"""
Flask web server for the Price Comparison Agent.
Provides REST API endpoints for the web interface.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import price_agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price_agent.scrapers import AmazonScraper, FlipkartScraper
from price_agent.recommender import Recommender
from price_agent.models import Product
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__, 
            template_folder='.',
            static_folder='static')
CORS(app)  # Enable CORS for API requests

# Initialize components - Only Amazon and Flipkart
scrapers = {
    "amazon": AmazonScraper(),
    "flipkart": FlipkartScraper()
}
recommender = Recommender()


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """
    Search for products and return recommendations.
    
    Request body:
        {
            "query": "product search query"
        }
    
    Response:
        {
            "recommendation": {
                "best_product": {...},
                "all_products": [...],
                "summary": "...",
                "detailed_analysis": "...",
                "timing_advice": "...",
                "alternative_suggestions": [...],
                "total_savings": 0.0
            }
        }
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Fetch products from all platforms concurrently
        all_products = fetch_all_products(query, max_results=3)
        
        if not all_products:
            return jsonify({'error': 'No products found'}), 404
        
        # Generate recommendation
        recommendation = recommender.generate_recommendation(all_products, query)
        
        # Convert to JSON-serializable format
        result = {
            'recommendation': {
                'best_product': product_to_dict(recommendation.best_product),
                'all_products': [product_to_dict(p) for p in recommendation.all_products],
                'summary': recommendation.summary,
                'detailed_analysis': recommendation.detailed_analysis,
                'timing_advice': recommendation.timing_advice,
                'alternative_suggestions': recommendation.alternative_suggestions,
                'total_savings': recommendation.total_savings,
                'savings_percentage': recommendation.savings_percentage,
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in search: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def fetch_all_products(query: str, max_results: int = 3):
    """Fetch products from all platforms concurrently"""
    all_products = []
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(scraper.search_product, query, max_results): platform
            for platform, scraper in scrapers.items()
        }
        
        for future in as_completed(futures):
            platform = futures[future]
            try:
                products = future.result()
                all_products.extend(products)
            except Exception as e:
                print(f"Error fetching from {platform}: {e}")
    
    return all_products


def product_to_dict(product: Product) -> dict:
    """Convert Product object to dictionary"""
    return {
        'name': product.name,
        'product_id': product.product_id,
        'platform': product.platform.value,
        'current_price': product.current_price,
        'original_price': product.original_price,
        'discount_percentage': product.discount_percentage,
        'url': product.url,
        'image_url': product.image_url,
        'in_stock': product.in_stock,
        'rating': product.rating,
        'total_reviews': product.total_reviews,
        'seller_info': {
            'name': product.seller_info.name if product.seller_info else 'Unknown',
            'rating': product.seller_info.rating if product.seller_info else 0,
            'trust_score': product.seller_info.get_trust_score() if product.seller_info else 0
        } if product.seller_info else None
    }


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Starting AI Price Comparison Web Server".center(70))
    print("="*70)
    print("\nServer running at: http://localhost:5000")
    print("Open your browser and visit the URL above\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
