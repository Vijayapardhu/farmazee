// Farmazee - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeComponents();
    
    // Setup event listeners
    setupEventListeners();
    
    // Initialize animations
    initializeAnimations();
});

// Initialize all components
function initializeComponents() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize notification system
    initializeNotifications();
}

// Setup event listeners
function setupEventListeners() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form submission handling
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
    
    // Auto-hide alerts
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('alert-dismissible')) {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            }
        }, 5000);
    });
    
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Initialize animations
function initializeAnimations() {
    // Add animation classes to elements when they come into view
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    animationObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            animationObserver.observe(el);
        });
    }
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('#search-input');
    const searchResults = document.querySelector('#search-results');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else {
                searchResults.style.display = 'none';
            }
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
}

// Perform search
function performSearch(query) {
    const searchResults = document.querySelector('#search-results');
    
    // Show loading state
    searchResults.innerHTML = '<div class="p-3 text-center"><div class="spinner"></div></div>';
    searchResults.style.display = 'block';
    
    // Make AJAX request to search endpoint
    fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data, searchResults);
        })
        .catch(error => {
            console.error('Search error:', error);
            searchResults.innerHTML = '<div class="p-3 text-center text-muted">Search failed. Please try again.</div>';
        });
}

// Display search results
function displaySearchResults(data, container) {
    let html = '';
    
    if (data.crops && data.crops.length > 0) {
        html += '<div class="search-section"><h6 class="text-muted">Crops</h6>';
        data.crops.forEach(crop => {
            html += `<a href="/crops/${crop.id}/" class="search-item">${crop.name}</a>`;
        });
        html += '</div>';
    }
    
    if (data.products && data.products.length > 0) {
        html += '<div class="search-section"><h6 class="text-muted">Products</h6>';
        data.products.forEach(product => {
            html += `<a href="/marketplace/product/${product.id}/" class="search-item">${product.name}</a>`;
        });
        html += '</div>';
    }
    
    if (data.schemes && data.schemes.length > 0) {
        html += '<div class="search-section"><h6 class="text-muted">Schemes</h6>';
        data.schemes.forEach(scheme => {
            html += `<a href="/schemes/${scheme.id}/" class="search-item">${scheme.title}</a>`;
        });
        html += '</div>';
    }
    
    if (html === '') {
        html = '<div class="p-3 text-center text-muted">No results found.</div>';
    }
    
    container.innerHTML = html;
}

// Notification system
function initializeNotifications() {
    // Mark notification as read
    document.querySelectorAll('.mark-read-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const notificationId = this.dataset.notificationId;
            markNotificationAsRead(notificationId, this);
        });
    });
    
    // Real-time notifications (if WebSocket is available)
    if ('WebSocket' in window) {
        initializeWebSocket();
    }
}

// Mark notification as read
function markNotificationAsRead(notificationId, button) {
    fetch(`/notifications/${notificationId}/read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const notificationCard = button.closest('.notification-card');
            notificationCard.style.opacity = '0.5';
            button.disabled = true;
            button.textContent = 'Read';
        }
    })
    .catch(error => {
        console.error('Error marking notification as read:', error);
    });
}

// WebSocket for real-time notifications (Disabled for now)
// Uncomment when Django Channels is configured
function initializeWebSocket() {
    // Disabled - configure Django Channels first
    console.log('WebSocket disabled - configure Django Channels to enable real-time notifications');
    return;
    
    /* Uncomment to enable
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
    
    try {
        const socket = new WebSocket(wsUrl);
        
        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.type === 'notification') {
                showNotification(data.message);
            }
        };
        
        socket.onclose = function() {
            // Reconnect after 5 seconds
            setTimeout(initializeWebSocket, 5000);
        };
    } catch (error) {
        console.log('WebSocket not available:', error);
    }
    */
}

// Show notification toast
function showNotification(message) {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        createToastContainer();
    }
    
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">Smart Farmer</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Create toast container
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
}

// Form submission handler
function handleFormSubmit(event) {
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        submitBtn.disabled = true;
        
        // Re-enable button after 10 seconds (fallback)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 10000);
    }
}

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Format currency
function formatCurrency(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Format date
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    return new Intl.DateTimeFormat('en-IN', { ...defaultOptions, ...options }).format(new Date(date));
}

// Show loading spinner
function showLoading(element) {
    element.innerHTML = '<div class="text-center"><div class="spinner"></div><p class="mt-2">Loading...</p></div>';
}

// Hide loading spinner
function hideLoading(element, content) {
    element.innerHTML = content;
}

// Show success message
function showSuccess(message, duration = 3000) {
    showAlert('success', message, duration);
}

// Show error message
function showError(message, duration = 5000) {
    showAlert('danger', message, duration);
}

// Show warning message
function showWarning(message, duration = 4000) {
    showAlert('warning', message, duration);
}

// Show info message
function showInfo(message, duration = 4000) {
    showAlert('info', message, duration);
}

// Show alert
function showAlert(type, message, duration) {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) {
        createAlertContainer();
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.getElementById('alert-container').appendChild(alert);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, duration);
}

// Create alert container
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alert-container';
    container.className = 'position-fixed top-0 start-50 translate-middle-x p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
}

// Export functions for global use
window.SmartFarmer = {
    showSuccess,
    showError,
    showWarning,
    showInfo,
    formatCurrency,
    formatDate,
    showLoading,
    hideLoading
};


