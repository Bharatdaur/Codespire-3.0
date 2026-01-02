"""
Demo script showing example usage of the Price Comparison Agent.
"""

from price_agent.scrapers import AmazonScraper, FlipkartScraper, MeeshoScraper
from price_agent.recommender import Recommender
from price_agent.formatter import OutputFormatter


def demo_search(query: str):
    """Run a demo search"""
    print(f"\n{'='*70}")
    print(f"Demo: Searching for '{query}'")
    print(f"{'='*70}\n")
    
    # Initialize components
    scrapers = [AmazonScraper(), FlipkartScraper(), MeeshoScraper()]
    recommender = Recommender()
    formatter = OutputFormatter()
    
    # Fetch products
    all_products = []
    for scraper in scrapers:
        products = scraper.search_product(query, max_results=2)
        all_products.extend(products)
    
    # Generate recommendation
    if all_products:
        recommendation = recommender.generate_recommendation(all_products, query)
        formatter.print_recommendation(recommendation)
    else:
        formatter.print_error("No products found")
    
    # Cleanup
    for scraper in scrapers:
        scraper.close()


if __name__ == "__main__":
    # Demo searches
    demo_search("laptop")
    
    print("\n" + "="*70)
    print("Demo completed!")
    print("="*70 + "\n")
