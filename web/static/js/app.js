// ===== STATE MANAGEMENT =====
let searchCount = 0;
let totalSavings = 0;

// ===== DOM ELEMENTS =====
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const quickTags = document.querySelectorAll('.quick-tag');

// ===== EVENT LISTENERS =====
searchForm.addEventListener('submit', handleSearch);

quickTags.forEach(tag => {
    tag.addEventListener('click', () => {
        searchInput.value = tag.dataset.query;
        handleSearch(new Event('submit'));
    });
});

// ===== SEARCH HANDLER =====
async function handleSearch(e) {
    e.preventDefault();

    const query = searchInput.value.trim();
    if (!query) return;

    // Update UI state
    showLoading();
    searchButton.classList.add('loading');

    try {
        // Call backend API
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        const data = await response.json();

        // Update stats
        searchCount++;
        totalSavings += data.recommendation.total_savings || 0;
        updateStats();

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Search error:', error);
        showError('Failed to fetch results. Please try again.');
    } finally {
        hideLoading();
        searchButton.classList.remove('loading');
    }
}

// ===== UI FUNCTIONS =====
function showLoading() {
    resultsSection.classList.add('hidden');
    loadingState.classList.remove('hidden');

    // Animate loading text
    const loadingTexts = [
        'Searching across Amazon & Flipkart',
        'Analyzing prices with AI...',
        'Comparing seller ratings...',
        'Calculating best deals...'
    ];

    let index = 0;
    const loadingTextEl = document.getElementById('loadingText');

    const interval = setInterval(() => {
        loadingTextEl.textContent = loadingTexts[index];
        index = (index + 1) % loadingTexts.length;
    }, 1500);

    // Store interval ID to clear later
    loadingState.dataset.intervalId = interval;
}

function hideLoading() {
    const intervalId = loadingState.dataset.intervalId;
    if (intervalId) {
        clearInterval(parseInt(intervalId));
    }
    loadingState.classList.add('hidden');
}

function updateStats() {
    document.getElementById('totalSearches').textContent = searchCount;
    document.getElementById('totalSavings').textContent = `₹${totalSavings.toLocaleString('en-IN')}`;
}

function displayResults(data) {
    const recommendation = data.recommendation;
    const bestProduct = recommendation.best_product;

    // Update best deal card
    document.getElementById('bestPlatform').textContent = bestProduct.platform.toUpperCase();
    document.getElementById('bestPrice').textContent = formatPrice(bestProduct.current_price);
    document.getElementById('bestOriginalPrice').textContent = `₹${formatPrice(bestProduct.original_price || 0)}`;
    document.getElementById('bestDiscount').textContent = `${bestProduct.discount_percentage.toFixed(1)}% OFF`;
    document.getElementById('savingsAmount').textContent = `₹${formatPrice(recommendation.total_savings)}`;
    document.getElementById('aiSummary').textContent = `💡 ${recommendation.summary || 'Great deal found!'}`;

    // Update recommendations
    document.getElementById('detailedAnalysis').textContent = recommendation.detailed_analysis || 'Analyzing...';
    document.getElementById('timingAdvice').textContent = recommendation.timing_advice || 'Buy now for best value!';

    // Update comparison table
    displayComparisonTable(recommendation.all_products, bestProduct);

    // Update tips
    displayTips(recommendation.alternative_suggestions || []);

    // Show results with animation
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayComparisonTable(products, bestProduct) {
    const table = document.getElementById('comparisonTable');

    let html = `
        <div class="product-row header">
            <div class="cell">Platform</div>
            <div class="cell">Price</div>
            <div class="cell">Discount</div>
            <div class="cell">Rating</div>
            <div class="cell">Seller</div>
            <div class="cell">Stock</div>
        </div>
    `;

    products.forEach(product => {
        const isBest = product.product_id === bestProduct.product_id;
        const rowClass = isBest ? 'product-row best' : 'product-row';

        html += `
            <div class="${rowClass}">
                <div class="cell" data-label="Platform">
                    ${isBest ? '🏆 ' : ''}<span class="platform-badge">${product.platform.toUpperCase()}</span>
                </div>
                <div class="cell" data-label="Price">₹${formatPrice(product.current_price)}</div>
                <div class="cell" data-label="Discount">${product.discount_percentage.toFixed(1)}%</div>
                <div class="cell" data-label="Rating">⭐ ${product.rating.toFixed(1)}</div>
                <div class="cell" data-label="Seller">${product.seller_info?.name || 'Unknown'}</div>
                <div class="cell" data-label="Stock">${product.in_stock ? '✅' : '❌'}</div>
            </div>
        `;
    });

    table.innerHTML = html;
}

function displayTips(suggestions) {
    const tipsGrid = document.getElementById('tipsGrid');

    if (!suggestions || suggestions.length === 0) {
        suggestions = [
            'Check seller ratings before purchasing',
            'Compare shipping costs',
            'Look for additional coupons',
            'Read product reviews carefully'
        ];
    }

    let html = '';
    suggestions.forEach(tip => {
        html += `<div class="tip-item">✨ ${tip}</div>`;
    });

    tipsGrid.innerHTML = html;
}

function formatPrice(price) {
    return price.toLocaleString('en-IN', { maximumFractionDigits: 2 });
}

function showError(message) {
    alert(message);
}

// ===== DEMO MODE (for testing without backend) =====
// Uncomment this to test the UI without the backend
/*
async function handleSearch(e) {
    e.preventDefault();
    
    const query = searchInput.value.trim();
    if (!query) return;
    
    showLoading();
    searchButton.classList.add('loading');
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock data
    const mockData = {
        recommendation: {
            best_product: {
                platform: 'meesho',
                current_price: 7923.56,
                original_price: 10106.61,
                discount_percentage: 21.6,
                rating: 4.2,
                product_id: 'mock123',
                in_stock: true,
                seller_info: { name: 'Smart Deals' }
            },
            all_products: [
                {
                    platform: 'amazon',
                    current_price: 9234.50,
                    discount_percentage: 15.3,
                    rating: 4.5,
                    product_id: 'amz1',
                    in_stock: true,
                    seller_info: { name: 'Amazon.in' }
                },
                {
                    platform: 'flipkart',
                    current_price: 8756.20,
                    discount_percentage: 18.7,
                    rating: 4.3,
                    product_id: 'flp1',
                    in_stock: true,
                    seller_info: { name: 'RetailNet' }
                },
                {
                    platform: 'meesho',
                    current_price: 7923.56,
                    discount_percentage: 21.6,
                    rating: 4.2,
                    product_id: 'mock123',
                    in_stock: true,
                    seller_info: { name: 'Smart Deals' }
                }
            ],
            total_savings: 1310.94,
            summary: 'Meesho offers the best value with significant savings compared to other platforms.',
            detailed_analysis: 'After analyzing prices across all platforms, Meesho provides the lowest price at ₹7,923.56, which is 14% cheaper than Amazon and 9% cheaper than Flipkart.',
            timing_advice: 'Buy now - the current discount is excellent and no major sales are expected in the next 14 days.',
            alternative_suggestions: [
                'Check return policy before purchasing',
                'Compare shipping costs and delivery time',
                'Look for bank offers or cashback deals'
            ]
        }
    };
    
    searchCount++;
    totalSavings += mockData.recommendation.total_savings;
    updateStats();
    displayResults(mockData);
    
    hideLoading();
    searchButton.classList.remove('loading');
}
*/

// ===== INITIALIZATION =====
console.log('🤖 AI Price Comparison loaded!');
