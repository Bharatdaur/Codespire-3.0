# 🤖 AI-Powered Price Comparison Agent

An intelligent price comparison tool that leverages **Gemini AI** to analyze product prices across **Amazon**, **Flipkart**, and **Meesho**. Get smart recommendations on the best deals and optimal purchase timing!

## ✨ Features

- 🔍 **Multi-Platform Search**: Compare prices across Amazon, Flipkart, and Meesho simultaneously
- 🤖 **AI-Powered Analysis**: Gemini AI provides intelligent insights and recommendations
- 📊 **Price Trend Analysis**: Track historical prices and identify trends
- 🔮 **Price Prediction**: Predict optimal purchase timing based on historical data
- 📅 **Sale Event Detection**: Get notified about upcoming sales (Diwali, Black Friday, etc.)
- ⭐ **Seller Trust Scoring**: Evaluate seller reliability across platforms
- 💰 **Savings Calculator**: See exactly how much you save with the best deal
- 🎨 **Beautiful CLI**: Rich, colorful terminal output with tables and panels

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your API key**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### Usage

**Basic search**:
```bash
python main.py "laptop"
```

**Search with multiple words**:
```bash
python main.py "wireless mouse"
python main.py "samsung smartphone"
python main.py "running shoes"
```

## 📖 How It Works

1. **Search**: Enter a product name
2. **Fetch**: Agent searches Amazon, Flipkart, and Meesho concurrently
3. **Analyze**: 
   - Compares prices across platforms
   - Analyzes historical price trends
   - Evaluates seller trustworthiness
   - Predicts future price movements
4. **AI Insights**: Gemini AI generates personalized recommendations
5. **Display**: Beautiful terminal output shows:
   - Best deal with savings
   - Price comparison table
   - Detailed analysis
   - When to buy advice
   - Alternative suggestions

## 🎯 Example Output

```
🎯 BEST DEAL FOUND

Platform: MEESHO
Price: ₹24,567.89 (was ₹35,432.10)
Discount: 30.7% OFF
You Save: ₹5,234.21 (17.5%)

💡 Meesho offers the best value with significant savings...

📊 Price Comparison Across Platforms
┌────────────┬──────────────┬──────────┬─────────┬────────────────┬─────────────┬──────────┐
│ Platform   │        Price │ Discount │  Rating │ Seller         │ Trust Score │    Stock │
├────────────┼──────────────┼──────────┼─────────┼────────────────┼─────────────┼──────────┤
│ 🏆 MEESHO  │  ₹24,567.89 │   30.7%  │ ⭐ 4.2  │ Smart Deals    │      82/100 │ ✅ In... │
│ AMAZON     │  ₹28,234.56 │   25.3%  │ ⭐ 4.5  │ Amazon.in      │      95/100 │ ✅ In... │
│ FLIPKART   │  ₹29,802.10 │   20.1%  │ ⭐ 4.3  │ RetailNet      │      88/100 │ ✅ In... │
└────────────┴──────────────┴──────────┴─────────┴────────────────┴─────────────┴──────────┘
```

## 🏗️ Architecture

```
price_agent/
├── __init__.py           # Package initialization
├── config.py             # Configuration management
├── models.py             # Data models
├── database.py           # SQLite database manager
├── scrapers/             # Platform scrapers
│   ├── base_scraper.py   # Base scraper class
│   ├── amazon_scraper.py # Amazon scraper
│   ├── flipkart_scraper.py # Flipkart scraper
│   └── meesho_scraper.py # Meesho scraper
├── analyzer.py           # Price analysis
├── predictor.py          # Price prediction
├── gemini_agent.py       # Gemini AI integration
├── recommender.py        # Recommendation engine
└── formatter.py          # Output formatting
```

## 🔧 Configuration

Edit `.env` file to customize:

```bash
# Required
GEMINI_API_KEY=your_key_here

# Optional
DATABASE_URL=sqlite:///price_history.db
REQUEST_DELAY=2
MAX_RETRIES=3
GEMINI_MODEL=gemini-1.5-flash
```

## 📊 Data Storage

The agent automatically stores:
- Product information
- Historical prices (30 days by default)
- Seller ratings
- Search history

Data is stored in SQLite database (`price_history.db`) for trend analysis.

## 🤝 Contributing

This is a demonstration project. To enhance it:

1. **Add real API integrations**: Replace mock data with actual API calls
2. **Implement web scraping**: Add BeautifulSoup-based scrapers
3. **Add more platforms**: Extend to other e-commerce sites
4. **Improve predictions**: Use advanced ML models
5. **Add GUI**: Create a web interface with Flask/FastAPI

## ⚠️ Legal Notice

This tool uses **mock data** for demonstration. For production use:
- Obtain proper API access from platforms
- Respect Terms of Service
- Implement rate limiting
- Use for personal/educational purposes only

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent analysis
- **Rich** library for beautiful terminal output
- **SQLAlchemy** for database management

## 💬 Support

For issues or questions:
1. Check the `.env.example` file for configuration
2. Ensure your Gemini API key is valid
3. Verify all dependencies are installed

---

**Made with ❤️ using Gemini AI**
