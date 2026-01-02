"""
Output formatter - Rich console formatting for beautiful output.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from typing import List
import matplotlib.pyplot as plt
from datetime import datetime

from .models import Recommendation, Product, PriceAnalysis


class OutputFormatter:
    """Formats output for terminal display"""
    
    def __init__(self):
        self.console = Console()
    
    def print_recommendation(self, recommendation: Recommendation):
        """Print comprehensive recommendation"""
        self.console.print()
        
        # Print summary
        self._print_summary(recommendation)
        
        # Print price comparison table
        self._print_price_table(recommendation.all_products, recommendation.best_product)
        
        # Print detailed analysis
        self._print_analysis(recommendation)
        
        # Print timing advice
        self._print_timing(recommendation)
        
        # Print alternative suggestions
        if recommendation.alternative_suggestions:
            self._print_suggestions(recommendation.alternative_suggestions)
        
        self.console.print()
    
    def _print_summary(self, recommendation: Recommendation):
        """Print summary panel"""
        best = recommendation.best_product
        
        # Create summary text
        summary_text = Text()
        summary_text.append("🎯 BEST DEAL FOUND\n\n", style="bold cyan")
        summary_text.append(f"Platform: ", style="white")
        summary_text.append(f"{best.platform.value.upper()}\n", style="bold green")
        summary_text.append(f"Price: ", style="white")
        summary_text.append(f"₹{best.current_price:,.2f}", style="bold yellow")
        
        if best.original_price and best.original_price > best.current_price:
            summary_text.append(f" (was ₹{best.original_price:,.2f})", style="dim")
            summary_text.append(f"\nDiscount: ", style="white")
            summary_text.append(f"{best.discount_percentage:.1f}% OFF", style="bold green")
        
        if recommendation.total_savings > 0:
            summary_text.append(f"\nYou Save: ", style="white")
            summary_text.append(f"₹{recommendation.total_savings:,.2f}", style="bold green")
            summary_text.append(f" ({recommendation.savings_percentage:.1f}%)", style="green")
        
        # Add AI summary
        if recommendation.summary:
            summary_text.append(f"\n\n💡 ", style="yellow")
            summary_text.append(recommendation.summary, style="white")
        
        panel = Panel(
            summary_text,
            title="[bold white]Price Comparison Results[/bold white]",
            border_style="cyan",
            box=box.DOUBLE
        )
        self.console.print(panel)
    
    def _print_price_table(self, products: List[Product], best_product: Product):
        """Print price comparison table"""
        table = Table(
            title="📊 Price Comparison Across Platforms",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("Platform", style="cyan", width=12)
        table.add_column("Price", justify="right", style="yellow")
        table.add_column("Discount", justify="right", style="green")
        table.add_column("Rating", justify="center")
        table.add_column("Seller", style="white", width=15)
        table.add_column("Trust Score", justify="center")
        table.add_column("Stock", justify="center")
        
        for product in products:
            is_best = product.product_id == best_product.product_id
            
            # Format values
            price = f"₹{product.current_price:,.2f}"
            discount = f"{product.discount_percentage:.1f}%" if product.discount_percentage > 0 else "-"
            rating = f"⭐ {product.rating:.1f}" if product.rating > 0 else "-"
            seller = product.seller_info.name[:15] if product.seller_info else "Unknown"
            trust = f"{product.seller_info.get_trust_score():.0f}/100" if product.seller_info else "-"
            stock = "✅ In Stock" if product.in_stock else "❌ Out"
            
            # Style for best product
            style = "bold green" if is_best else "white"
            
            table.add_row(
                f"{'🏆 ' if is_best else ''}{product.platform.value.upper()}",
                price,
                discount,
                rating,
                seller,
                trust,
                stock,
                style=style
            )
        
        self.console.print(table)
    
    def _print_analysis(self, recommendation: Recommendation):
        """Print detailed analysis"""
        if not recommendation.detailed_analysis:
            return
        
        analysis_text = Text()
        analysis_text.append("📈 Detailed Analysis\n\n", style="bold magenta")
        analysis_text.append(recommendation.detailed_analysis, style="white")
        
        # Add price trend if available
        if recommendation.price_analysis:
            analysis = recommendation.price_analysis
            analysis_text.append(f"\n\n📊 Price Statistics:\n", style="bold white")
            analysis_text.append(f"  • Current: ₹{analysis.current_price:,.2f}\n", style="white")
            analysis_text.append(f"  • Average: ₹{analysis.avg_price:,.2f}\n", style="white")
            analysis_text.append(f"  • Lowest: ₹{analysis.min_price:,.2f}\n", style="green")
            analysis_text.append(f"  • Highest: ₹{analysis.max_price:,.2f}\n", style="red")
            analysis_text.append(f"  • Trend: {analysis.trend.value.upper()}\n", style="cyan")
            analysis_text.append(f"  • Price Position: {analysis.get_price_position().upper()}", style="yellow")
        
        panel = Panel(analysis_text, border_style="magenta", box=box.ROUNDED)
        self.console.print(panel)
    
    def _print_timing(self, recommendation: Recommendation):
        """Print timing advice"""
        if not recommendation.timing_advice:
            return
        
        timing_text = Text()
        timing_text.append("⏰ When to Buy\n\n", style="bold blue")
        timing_text.append(recommendation.timing_advice, style="white")
        
        # Add prediction details if available
        if recommendation.prediction:
            pred = recommendation.prediction
            timing_text.append(f"\n\n🔮 Prediction:\n", style="bold white")
            timing_text.append(f"  • Confidence: {pred.confidence:.0f}%\n", style="white")
            
            if pred.upcoming_sale:
                timing_text.append(f"  • Upcoming Sale: {pred.upcoming_sale}\n", style="yellow")
                timing_text.append(f"  • Days Until Sale: {pred.days_until_sale}\n", style="yellow")
            
            if pred.expected_price_drop > 0:
                timing_text.append(f"  • Expected Drop: ₹{pred.expected_price_drop:,.2f}\n", style="green")
            
            timing_text.append(f"  • Recommendation: {pred.recommendation}", style="bold cyan")
        
        panel = Panel(timing_text, border_style="blue", box=box.ROUNDED)
        self.console.print(panel)
    
    def _print_suggestions(self, suggestions: List[str]):
        """Print alternative suggestions"""
        suggestion_text = Text()
        suggestion_text.append("💡 Additional Tips\n\n", style="bold yellow")
        
        for i, suggestion in enumerate(suggestions, 1):
            suggestion_text.append(f"  {i}. {suggestion}\n", style="white")
        
        panel = Panel(suggestion_text, border_style="yellow", box=box.ROUNDED)
        self.console.print(panel)
    
    def print_error(self, message: str):
        """Print error message"""
        self.console.print(f"\n❌ [bold red]Error:[/bold red] {message}\n")
    
    def print_info(self, message: str):
        """Print info message"""
        self.console.print(f"ℹ️  [cyan]{message}[/cyan]")
    
    def print_success(self, message: str):
        """Print success message"""
        self.console.print(f"✅ [bold green]{message}[/bold green]")
