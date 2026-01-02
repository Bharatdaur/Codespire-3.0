# Quick Setup Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure API Key

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

To get a free Gemini API key:
- Visit: https://makersuite.google.com/app/apikey
- Sign in with your Google account
- Click "Create API Key"
- Copy the key and paste it in your `.env` file

## Step 3: Run the Agent

Search for any product:
```bash
python main.py "laptop"
python main.py "wireless mouse"
python main.py "smartphone"
```

## Step 4: View Results

The agent will:
1. Search Amazon, Flipkart, and Meesho
2. Compare prices and analyze trends
3. Use Gemini AI for intelligent recommendations
4. Display beautiful results in your terminal

## Troubleshooting

**Error: GEMINI_API_KEY is required**
- Make sure you created a `.env` file (not `.env.example`)
- Verify your API key is correct
- No quotes needed around the API key in `.env`

**Error: Module not found**
- Run `pip install -r requirements.txt` again
- Make sure you're in the correct directory

**No products found**
- Try a different search query
- The mock data generator creates random products

## Example Commands

```bash
# Basic search
python main.py laptop

# Multi-word search
python main.py "gaming laptop"
python main.py "wireless headphones"

# Run demo
python examples/demo.py
```

Enjoy smart shopping! 🛍️
