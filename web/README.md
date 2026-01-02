# AI Price Comparison - Web Interface

## 🌐 Running the Web Interface

### Quick Start

1. **Install dependencies** (if not already done):
```bash
pip install -r requirements.txt
```

2. **Make sure your `.env` file has the Gemini API key**:
```
GEMINI_API_KEY=your_key_here
```

3. **Start the web server**:
```bash
cd web
python app.py
```

4. **Open your browser**:
```
http://localhost:5000
```

## ✨ Features

- **🎨 Modern Glassmorphism Design**: Beautiful, premium UI with animated gradients
- **🔍 Real-time Search**: Search products across Amazon, Flipkart & Meesho
- **🤖 AI-Powered Insights**: Gemini AI provides intelligent recommendations
- **📊 Interactive Comparison**: Visual price comparison table
- **💰 Savings Calculator**: See exactly how much you save
- **📱 Fully Responsive**: Works perfectly on mobile, tablet, and desktop
- **⚡ Smooth Animations**: Delightful micro-interactions throughout

## 🎯 How to Use

1. Enter a product name in the search box (e.g., "laptop", "smartphone")
2. Click "Search Now" or press Enter
3. Wait for AI to analyze prices across platforms
4. View the best deal with detailed recommendations
5. Compare prices in the interactive table
6. Get smart shopping tips

## 🏗️ Architecture

```
web/
├── app.py              # Flask backend server
├── index.html          # Main HTML page
└── static/
    ├── css/
    │   └── style.css   # Glassmorphism styles
    └── js/
        └── app.js      # Frontend JavaScript
```

## 🔧 API Endpoints

### POST /api/search
Search for products and get recommendations.

**Request:**
```json
{
  "query": "laptop"
}
```

**Response:**
```json
{
  "recommendation": {
    "best_product": {...},
    "all_products": [...],
    "summary": "AI-generated summary",
    "detailed_analysis": "...",
    "timing_advice": "...",
    "alternative_suggestions": [...],
    "total_savings": 1234.56
  }
}
```

### GET /api/health
Health check endpoint.

## 🎨 Design Features

- **Animated Background**: Floating gradient orbs
- **Glassmorphism Cards**: Frosted glass effect with blur
- **Smooth Transitions**: 300ms cubic-bezier animations
- **Responsive Grid**: Auto-fit columns for all screen sizes
- **Color Gradients**: Purple, pink, and blue gradient themes
- **Micro-animations**: Hover effects, loading spinners, progress bars

## 🚀 Production Deployment

For production, consider:

1. **Use a production WSGI server**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Add environment variables**:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
```

3. **Enable HTTPS** with a reverse proxy (nginx/Apache)

4. **Add rate limiting** to prevent abuse

## 💡 Tips

- The web interface uses the same Python backend as the CLI
- All searches are saved to the database for price history
- You can customize colors in `style.css` CSS variables
- The demo mode in `app.js` can be enabled for testing without backend

Enjoy smart shopping! 🛍️✨
