/**
 * FARMazee - Marketplace JavaScript
 * Handles marketplace functionality
 */

// Marketplace state
let marketplaceData = {
    products: [],
    categories: [],
    cart: [],
    orders: []
};

// Initialize marketplace functionality
document.addEventListener('DOMContentLoaded', function() {
    initMarketplace();
});

/**
 * Initialize marketplace functionality
 */
function initMarketplace() {
    loadMarketplaceData();
    setupMarketplaceUpdates();
}

/**
 * Load marketplace data
 */
async function loadMarketplaceData() {
    try {
        const [products, categories, orders] = await Promise.all([
            loadProducts(),
            loadCategories(),
            loadOrders()
        ]);
        
        marketplaceData.products = products;
        marketplaceData.categories = categories;
        marketplaceData.orders = orders;
        
        renderMarketplaceData();
        
    } catch (error) {
        console.error('Error loading marketplace data:', error);
        showMarketplaceError('Failed to load marketplace data');
    }
}

/**
 * Load products
 */
async function loadProducts() {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return [
        {
            id: 1,
            name: 'Organic Fertilizer',
            category: 'Fertilizers',
            price: 25.99,
            description: 'High-quality organic fertilizer for all crops',
            image: '🌱',
            rating: 4.5,
            reviews: 128,
            inStock: true,
            seller: 'Green Farms Ltd'
        },
        {
            id: 2,
            name: 'Drip Irrigation Kit',
            category: 'Irrigation',
            price: 89.99,
            description: 'Complete drip irrigation system for 1 acre',
            image: '💧',
            rating: 4.8,
            reviews: 95,
            inStock: true,
            seller: 'WaterTech Solutions'
        }
    ];
}

/**
 * Load categories
 */
async function loadCategories() {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return [
        { id: 1, name: 'Seeds', icon: '🌱' },
        { id: 2, name: 'Fertilizers', icon: '🌿' },
        { id: 3, name: 'Pesticides', icon: '🦗' },
        { id: 4, name: 'Irrigation', icon: '💧' },
        { id: 5, name: 'Equipment', icon: '🚜' },
        { id: 6, name: 'Tools', icon: '🔧' }
    ];
}

/**
 * Load orders
 */
async function loadOrders() {
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return [
        {
            id: 1,
            productName: 'Organic Fertilizer',
            quantity: 2,
            total: 51.98,
            status: 'delivered',
            orderDate: '2025-01-25'
        }
    ];
}

/**
 * Render marketplace data
 */
function renderMarketplaceData() {
    renderCategories();
    renderProducts();
    renderOrders();
    renderCart();
}

/**
 * Render categories
 */
function renderCategories() {
    const container = document.querySelector('.marketplace-categories');
    if (!container) return;
    
    container.innerHTML = `
        <h3>Product Categories</h3>
        <div class="categories-grid">
            ${marketplaceData.categories.map(category => `
                <div class="category-card" onclick="filterByCategory('${category.name}')">
                    <div class="category-icon">${category.icon}</div>
                    <h4>${category.name}</h4>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render products
 */
function renderProducts() {
    const container = document.querySelector('.marketplace-products');
    if (!container) return;
    
    container.innerHTML = `
        <h3>Available Products</h3>
        <div class="products-grid">
            ${marketplaceData.products.map(product => `
                <div class="product-card">
                    <div class="product-image">${product.image}</div>
                    <div class="product-content">
                        <h4>${product.name}</h4>
                        <p class="product-description">${product.description}</p>
                        <div class="product-rating">
                            <span class="stars">${'⭐'.repeat(Math.floor(product.rating))}</span>
                            <span class="rating-text">${product.rating} (${product.reviews} reviews)</span>
                        </div>
                        <div class="product-seller">
                            <i class="fas fa-store"></i>
                            <span>${product.seller}</span>
                        </div>
                        <div class="product-price">
                            <span class="price">$${product.price}</span>
                            <span class="stock ${product.inStock ? 'in-stock' : 'out-of-stock'}">
                                ${product.inStock ? 'In Stock' : 'Out of Stock'}
                            </span>
                        </div>
                        <div class="product-actions">
                            <button class="btn btn-primary" onclick="addToCart(${product.id})" ${!product.inStock ? 'disabled' : ''}>
                                <i class="fas fa-cart-plus"></i>
                                Add to Cart
                            </button>
                            <button class="btn btn-secondary" onclick="viewProduct(${product.id})">
                                <i class="fas fa-eye"></i>
                                View
                            </button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render orders
 */
function renderOrders() {
    const container = document.querySelector('.marketplace-orders');
    if (!container) return;
    
    if (marketplaceData.orders.length === 0) {
        container.innerHTML = `
            <h3>Your Orders</h3>
            <p class="no-orders">No orders yet. Start shopping!</p>
        `;
        return;
    }
    
    container.innerHTML = `
        <h3>Your Orders</h3>
        <div class="orders-list">
            ${marketplaceData.orders.map(order => `
                <div class="order-item ${order.status}">
                    <div class="order-header">
                        <h4>${order.productName}</h4>
                        <span class="order-status ${order.status}">${order.status}</span>
                    </div>
                    <div class="order-details">
                        <p><strong>Quantity:</strong> ${order.quantity}</p>
                        <p><strong>Total:</strong> $${order.total}</p>
                        <p><strong>Order Date:</strong> ${formatDate(order.orderDate)}</p>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render cart
 */
function renderCart() {
    const container = document.querySelector('.marketplace-cart');
    if (!container) return;
    
    if (marketplaceData.cart.length === 0) {
        container.innerHTML = `
            <h3>Shopping Cart</h3>
            <p class="empty-cart">Your cart is empty. Add some products!</p>
        `;
        return;
    }
    
    const total = marketplaceData.cart.reduce((sum, item) => sum + item.total, 0);
    
    container.innerHTML = `
        <h3>Shopping Cart</h3>
        <div class="cart-items">
            ${marketplaceData.cart.map(item => `
                <div class="cart-item">
                    <div class="cart-item-image">${item.image}</div>
                    <div class="cart-item-content">
                        <h4>${item.name}</h4>
                        <p>$${item.price} x ${item.quantity}</p>
                    </div>
                    <div class="cart-item-total">$${item.total}</div>
                    <button class="btn-icon" onclick="removeFromCart(${item.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `).join('')}
        </div>
        <div class="cart-total">
            <h4>Total: $${total.toFixed(2)}</h4>
            <button class="btn btn-primary" onclick="checkout()">
                <i class="fas fa-credit-card"></i>
                Checkout
            </button>
        </div>
    `;
}

/**
 * Add product to cart
 */
function addToCart(productId) {
    const product = marketplaceData.products.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = marketplaceData.cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
        existingItem.total = existingItem.price * existingItem.quantity;
    } else {
        marketplaceData.cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1,
            total: product.price,
            image: product.image
        });
    }
    
    renderCart();
    
    if (window.Farmazee && window.Farmazee.showNotification) {
        window.Farmazee.showNotification('Product added to cart!', 'success');
    }
}

/**
 * Remove product from cart
 */
function removeFromCart(productId) {
    marketplaceData.cart = marketplaceData.cart.filter(item => item.id !== productId);
    renderCart();
    
    if (window.Farmazee && window.Farmazee.showNotification) {
        window.Farmazee.showNotification('Product removed from cart!', 'info');
    }
}

/**
 * Filter products by category
 */
function filterByCategory(categoryName) {
    const filteredProducts = categoryName === 'all' 
        ? marketplaceData.products 
        : marketplaceData.products.filter(product => product.category === categoryName);
    
    renderFilteredProducts(filteredProducts);
}

/**
 * Render filtered products
 */
function renderFilteredProducts(products) {
    const container = document.querySelector('.marketplace-products');
    if (!container) return;
    
    if (products.length === 0) {
        container.innerHTML = `
            <h3>No Products Found</h3>
            <p>No products available in this category.</p>
        `;
        return;
    }
    
    container.innerHTML = `
        <h3>Products in Category</h3>
        <div class="products-grid">
            ${products.map(product => `
                <div class="product-card">
                    <div class="product-image">${product.image}</div>
                    <div class="product-content">
                        <h4>${product.name}</h4>
                        <p class="product-description">${product.description}</p>
                        <div class="product-price">
                            <span class="price">$${product.price}</span>
                        </div>
                        <div class="product-actions">
                            <button class="btn btn-primary" onclick="addToCart(${product.id})">
                                <i class="fas fa-cart-plus"></i>
                                Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * View product details
 */
function viewProduct(productId) {
    const product = marketplaceData.products.find(p => p.id === productId);
    if (!product) return;
    
    showProductModal(product);
}

/**
 * Show product modal
 */
function showProductModal(product) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <div class="product-modal">
                <div class="product-modal-image">${product.image}</div>
                <div class="product-modal-content">
                    <h2>${product.name}</h2>
                    <p class="product-description">${product.description}</p>
                    <div class="product-details">
                        <p><strong>Category:</strong> ${product.category}</p>
                        <p><strong>Seller:</strong> ${product.seller}</p>
                        <p><strong>Rating:</strong> ${product.rating} ⭐ (${product.reviews} reviews)</p>
                        <p><strong>Price:</strong> $${product.price}</p>
                        <p><strong>Stock:</strong> <span class="${product.inStock ? 'in-stock' : 'out-of-stock'}">${product.inStock ? 'In Stock' : 'Out of Stock'}</span></p>
                    </div>
                    <div class="product-actions">
                        <button class="btn btn-primary" onclick="addToCart(${product.id})" ${!product.inStock ? 'disabled' : ''}>
                            <i class="fas fa-cart-plus"></i>
                            Add to Cart
                        </button>
                        <button class="btn btn-secondary" onclick="this.closest('.modal').remove()">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal functionality
    const closeBtn = modal.querySelector('.close');
    closeBtn.onclick = () => modal.remove();
    
    // Close modal when clicking outside
    modal.onclick = (e) => {
        if (e.target === modal) modal.remove();
    };
}

/**
 * Checkout process
 */
async function checkout() {
    if (marketplaceData.cart.length === 0) {
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification('Your cart is empty!', 'warning');
        }
        return;
    }
    
    try {
        // Simulate checkout process
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Create order
        const order = {
            id: Date.now(),
            productName: marketplaceData.cart[0].name,
            quantity: marketplaceData.cart[0].quantity,
            total: marketplaceData.cart[0].total,
            status: 'processing',
            orderDate: new Date().toISOString().split('T')[0]
        };
        
        marketplaceData.orders.push(order);
        marketplaceData.cart = [];
        
        renderCart();
        renderOrders();
        
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification('Order placed successfully!', 'success');
        }
        
    } catch (error) {
        console.error('Checkout error:', error);
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification('Checkout failed. Please try again.', 'error');
        }
    }
}

/**
 * Setup marketplace updates
 */
function setupMarketplaceUpdates() {
    // Update product availability every hour
    setInterval(updateProductAvailability, 60 * 60 * 1000);
}

/**
 * Update product availability
 */
function updateProductAvailability() {
    marketplaceData.products.forEach(product => {
        // Simulate stock changes
        if (Math.random() > 0.8) {
            product.inStock = !product.inStock;
        }
    });
    
    renderProducts();
}

/**
 * Show marketplace error
 */
function showMarketplaceError(message) {
    const container = document.querySelector('.marketplace-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="error-state">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Marketplace Unavailable</h3>
            <p>${message}</p>
            <button class="btn btn-primary" onclick="loadMarketplaceData()">
                <i class="fas fa-refresh"></i>
                Try Again
            </button>
        </div>
    `;
}

/**
 * Utility functions
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Export functions for use in other modules
window.Marketplace = {
    initMarketplace,
    loadMarketplaceData,
    renderMarketplaceData,
    addToCart,
    removeFromCart,
    filterByCategory,
    viewProduct,
    checkout
};

