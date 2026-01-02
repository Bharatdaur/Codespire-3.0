"""
Main application entry point.
Orchestrates the entire price comparison workflow.
"""

import sys
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from price_agent.scrapers import AmazonScraper, FlipkartScraper
from price_agent.recommender import Recommender
from price_agent.formatter import OutputFormatter
from price_agent.models import Product
from price_agent.config import Config


class PriceComparisonAgent:
    """Main price comparison agent"""
    
    def __init__(self):
        """Initialize the agent"""
        self.scrapers = {
            "amazon": AmazonScraper(),
            "flipkart": FlipkartScraper()
        }
        self.recommender = Recommender()
        self.formatter = OutputFormatter()
    
    def search_and_compare(self, query: str, max_results: int = 3) -> None:
        """
        Search for products and generate recommendations.
        
        Args:
            query: Product search query
            max_results: Maximum results per platform
        """
        self.formatter.print_info(f"🔍 Searching for: {query}")
        self.formatter.print_info(f"📡 Fetching prices from Amazon & Flipkart...\n")
        
        # Fetch products from all platforms concurrently
        all_products = self._fetch_all_products(query, max_results)
        
        if not all_products:
            self.formatter.print_error("No products found. Please try a different search query.")
            return
        
        self.formatter.print_success(f"Found {len(all_products)} products across {len(set(p.platform for p in all_products))} platforms\n")
        
        # Generate AI-powered recommendation
        self.formatter.print_info("🤖 Analyzing prices with Gemini AI...\n")
        
        try:
            recommendation = self.recommender.generate_recommendation(all_products, query)
            
            # Display results
            self.formatter.print_recommendation(recommendation)
            
        except Exception as e:
            self.formatter.print_error(f"Failed to generate recommendation: {e}")
            import traceback
            traceback.print_exc()
    
    def _fetch_all_products(self, query: str, max_results: int) -> List[Product]:
        """
        Fetch products from all platforms concurrently.
        
        Args:
            query: Search query
            max_results: Max results per platform
            
        Returns:
            List of all products
        """
        all_products = []
        
        # Use ThreadPoolExecutor for concurrent fetching
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit tasks
            futures = {
                executor.submit(scraper.search_product, query, max_results): platform
                for platform, scraper in self.scrapers.items()
            }
            
            # Collect results
            for future in as_completed(futures):
                platform = futures[future]
                try:
                    products = future.result()
                    all_products.extend(products)
                except Exception as e:
                    print(f"⚠️  Error fetching from {platform}: {e}")
        
        return all_products
    
    def close(self):
        """Clean up resources"""
        for scraper in self.scrapers.values():
            scraper.close()


def main():
    """Main entry point"""
    # Print banner
    print("\n" + "="*70)
    print("🤖 AI-Powered Price Comparison Agent".center(70))
    print("Compare prices across Amazon & Flipkart".center(70))
    print("="*70 + "\n")
    
    # Check if query provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <product_name>")
        print("Example: python main.py \"laptop\"")
        print("Example: python main.py \"wireless mouse\"")
        sys.exit(1)
    
    # Get search query from command line
    query = " ".join(sys.argv[1:])
    
    try:
        # Validate configuration
        Config.validate()
        
        # Create and run agent
        agent = PriceComparisonAgent()
        agent.search_and_compare(query)
        agent.close()
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n💡 Please set your GEMINI_API_KEY in a .env file")
        print("   Copy .env.example to .env and add your API key\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
