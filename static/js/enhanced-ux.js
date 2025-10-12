/**
 * Enhanced UX JavaScript - Smooth Interactions & Flow
 */

// ============================================
// SMOOTH PAGE TRANSITIONS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to page content
    const pageContent = document.querySelector('.page-content') || document.body;
    pageContent.style.animation = 'fadeInUp 0.5s ease-out';
    
    // Smooth scroll to top button
    createScrollToTopButton();
    
    // Enhanced tooltips
    initializeTooltips();
    
    // Form enhancements
    enhanceForms();
    
    // Card animations
    animateCards();
    
    // Enhanced modals
    enhanceModals();
    
    // Navigation flow
    enhanceNavigation();
});

// ============================================
// SCROLL TO TOP BUTTON
// ============================================

function createScrollToTopButton() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 6rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    `;
    
    document.body.appendChild(scrollBtn);
    
    // Show/hide on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    });
    
    // Scroll to top on click
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Hover effect
    scrollBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) translateY(-2px)';
    });
    
    scrollBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) translateY(0)';
    });
}

// ============================================
// ENHANCED TOOLTIPS
// ============================================

function initializeTooltips() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ============================================
// FORM ENHANCEMENTS
// ============================================

function enhanceForms() {
    // Add floating label effect
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
        
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
    
    // Real-time validation
    document.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.checkValidity()) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            } else {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            }
        });
        
        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                } else {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                }
            }
        });
    });
    
    // Form submission feedback
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && this.checkValidity()) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;
            }
        });
    });
}

// ============================================
// CARD ANIMATIONS
// ============================================

function animateCards() {
    const cards = document.querySelectorAll('.card, .stats-card, .big-tool-card, .quick-view-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.animation = 'fadeInUp 0.5s ease-out forwards';
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        observer.observe(card);
    });
}

// ============================================
// ENHANCED MODALS
// ============================================

function enhanceModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            this.style.animation = 'fadeIn 0.3s ease-out';
        });
        
        modal.addEventListener('hide.bs.modal', function() {
            this.style.animation = 'fadeOut 0.3s ease-out';
        });
    });
}

// ============================================
// NAVIGATION FLOW
// ============================================

function enhanceNavigation() {
    // Highlight active page in navigation
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Add page transition on navigation
    document.querySelectorAll('a:not([target="_blank"])').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href && !this.href.startsWith('#') && !this.href.includes('javascript:')) {
                const currentDomain = window.location.origin;
                if (this.href.startsWith(currentDomain)) {
                    // Same domain navigation - add transition
                    document.body.style.opacity = '0.8';
                }
            }
        });
    });
}

// ============================================
// QUICK SEARCH FUNCTIONALITY
// ============================================

function initializeQuickSearch() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    
    searchInputs.forEach(input => {
        // Add search icon
        const wrapper = document.createElement('div');
        wrapper.className = 'search-wrapper position-relative';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);
        
        const icon = document.createElement('i');
        icon.className = 'fas fa-search search-icon';
        icon.style.cssText = `
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: #6c757d;
            pointer-events: none;
        `;
        wrapper.appendChild(icon);
        
        input.style.paddingLeft = '2.5rem';
        
        // Live search indicator
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                icon.className = 'fas fa-spinner fa-spin search-icon';
                setTimeout(() => {
                    icon.className = 'fas fa-check search-icon';
                    icon.style.color = '#28a745';
                }, 500);
            } else {
                icon.className = 'fas fa-search search-icon';
                icon.style.color = '#6c757d';
            }
        });
    });
}

// ============================================
// ENHANCED TABLES
// ============================================

function enhanceTables() {
    document.querySelectorAll('.table tbody tr').forEach(row => {
        row.addEventListener('click', function(e) {
            // Don't trigger if clicking on button or link
            if (!e.target.closest('button, a')) {
                this.style.background = '#f8f9fa';
                setTimeout(() => {
                    this.style.background = '';
                }, 200);
            }
        });
    });
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.style.cssText = `
        position: fixed;
        top: 5rem;
        right: 1rem;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// ============================================
// LOADING OVERLAY
// ============================================

function showLoadingOverlay(message = 'Loading...') {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease-out;
    `;
    overlay.innerHTML = `
        <div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">${message}</p>
    `;
    
    document.body.appendChild(overlay);
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => overlay.remove(), 300);
    }
}

// ============================================
// ENHANCED CONFIRMATIONS
// ============================================

function confirmAction(message, callback) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="fas fa-exclamation-triangle me-2"></i>Confirm Action</h5>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger confirm-btn">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.querySelector('.confirm-btn').addEventListener('click', function() {
        callback();
        bsModal.hide();
        setTimeout(() => modal.remove(), 300);
    });
    
    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
    });
}

// ============================================
// DATA TABLE ENHANCEMENTS
// ============================================

function enhanceDataTables() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        // Add hover effect to rows
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.animationDelay = `${index * 50}ms`;
            row.style.animation = 'fadeInUp 0.5s ease-out forwards';
        });
        
        // Add sorting indicators (visual only)
        const headers = table.querySelectorAll('thead th');
        headers.forEach(header => {
            if (!header.querySelector('input, button')) {
                header.style.cursor = 'pointer';
                header.addEventListener('click', function() {
                    this.style.color = '#28a745';
                    setTimeout(() => {
                        this.style.color = '';
                    }, 300);
                });
            }
        });
    });
}

// ============================================
// PROGRESS TRACKING
// ============================================

function updateProgress(elementId, percentage) {
    const progressBar = document.getElementById(elementId);
    if (progressBar) {
        progressBar.style.width = '0%';
        setTimeout(() => {
            progressBar.style.width = percentage + '%';
            progressBar.style.transition = 'width 1s ease-out';
        }, 100);
    }
}

// ============================================
// BREADCRUMB AUTO-GENERATION
// ============================================

function generateBreadcrumbs() {
    const path = window.location.pathname;
    const parts = path.split('/').filter(p => p);
    
    if (parts.length > 1) {
        let breadcrumbHTML = '<nav aria-label="breadcrumb"><ol class="breadcrumb">';
        breadcrumbHTML += '<li class="breadcrumb-item"><a href="/"><i class="fas fa-home"></i> Home</a></li>';
        
        let currentPath = '';
        parts.forEach((part, index) => {
            currentPath += '/' + part;
            const isLast = index === parts.length - 1;
            const displayName = part.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            if (isLast) {
                breadcrumbHTML += `<li class="breadcrumb-item active">${displayName}</li>`;
            } else {
                breadcrumbHTML += `<li class="breadcrumb-item"><a href="${currentPath}">${displayName}</a></li>`;
            }
        });
        
        breadcrumbHTML += '</ol></nav>';
        
        const container = document.querySelector('.breadcrumb-container');
        if (container) {
            container.innerHTML = breadcrumbHTML;
        }
    }
}

// ============================================
// STATS COUNTER ANIMATION
// ============================================

function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

function animateAllCounters() {
    document.querySelectorAll('.stats-number').forEach(counter => {
        const target = parseInt(counter.textContent);
        if (!isNaN(target)) {
            counter.textContent = '0';
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(counter, target);
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(counter);
        }
    });
}

// ============================================
// SMART NAVIGATION FLOW
// ============================================

function createNavigationFlow() {
    // Add "Next Step" suggestions based on current page
    const currentPath = window.location.pathname;
    let nextStep = null;
    
    const flowMap = {
        '/': { next: '/signup/', text: 'Get Started - Sign Up' },
        '/signup/': { next: '/login/', text: 'Already have account? Login' },
        '/login/': { next: '/dashboard/', text: 'Go to Dashboard' },
        '/dashboard/': { next: '/ai-chatbot/chat/', text: 'Try AI Assistant' },
        '/ai-chatbot/chat/': { next: '/weather/', text: 'Check Weather' },
        '/weather/': { next: '/marketplace/', text: 'View Market Prices' },
        '/marketplace/': { next: '/schemes/', text: 'Explore Government Schemes' },
        '/schemes/': { next: '/problems/', text: 'Ask Expert' },
        '/problems/': { next: '/community/', text: 'Join Community' },
        '/admin-panel/': { next: '/admin-panel/users/', text: 'Manage Users' },
        '/admin-panel/users/': { next: '/admin-panel/content-moderation/', text: 'Moderate Content' },
    };
    
    if (flowMap[currentPath]) {
        const suggestion = document.createElement('div');
        suggestion.className = 'next-step-suggestion';
        suggestion.style.cssText = `
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            z-index: 998;
            animation: slideUp 0.5s ease-out;
        `;
        suggestion.innerHTML = `
            <span class="text-muted me-2">Next:</span>
            <a href="${flowMap[currentPath].next}" class="btn btn-sm btn-success">
                ${flowMap[currentPath].text} <i class="fas fa-arrow-right ms-2"></i>
            </a>
        `;
        
        document.body.appendChild(suggestion);
    }
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], input[name="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// ============================================
// INITIALIZE ON LOAD
// ============================================

window.addEventListener('load', function() {
    // Remove loading overlay if present
    hideLoadingOverlay();
    
    // Animate counters
    animateAllCounters();
    
    // Enhance data tables
    enhanceDataTables();
    
    // Initialize quick search
    initializeQuickSearch();
    
    // Create navigation flow
    createNavigationFlow();
    
    // Show success message for page load
    console.log('✅ Enhanced UX loaded successfully');
});

// ============================================
// EXPORT FUNCTIONS
// ============================================

window.FarmazeeUX = {
    showNotification,
    showLoadingOverlay,
    hideLoadingOverlay,
    confirmAction,
    updateProgress,
    animateCounter
};
 * Enhanced UX JavaScript - Smooth Interactions & Flow
 */

// ============================================
// SMOOTH PAGE TRANSITIONS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to page content
    const pageContent = document.querySelector('.page-content') || document.body;
    pageContent.style.animation = 'fadeInUp 0.5s ease-out';
    
    // Smooth scroll to top button
    createScrollToTopButton();
    
    // Enhanced tooltips
    initializeTooltips();
    
    // Form enhancements
    enhanceForms();
    
    // Card animations
    animateCards();
    
    // Enhanced modals
    enhanceModals();
    
    // Navigation flow
    enhanceNavigation();
});

// ============================================
// SCROLL TO TOP BUTTON
// ============================================

function createScrollToTopButton() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 6rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    `;
    
    document.body.appendChild(scrollBtn);
    
    // Show/hide on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    });
    
    // Scroll to top on click
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Hover effect
    scrollBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) translateY(-2px)';
    });
    
    scrollBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) translateY(0)';
    });
}

// ============================================
// ENHANCED TOOLTIPS
// ============================================

function initializeTooltips() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ============================================
// FORM ENHANCEMENTS
// ============================================

function enhanceForms() {
    // Add floating label effect
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
        
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
    
    // Real-time validation
    document.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.checkValidity()) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            } else {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            }
        });
        
        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                } else {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                }
            }
        });
    });
    
    // Form submission feedback
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && this.checkValidity()) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;
            }
        });
    });
}

// ============================================
// CARD ANIMATIONS
// ============================================

function animateCards() {
    const cards = document.querySelectorAll('.card, .stats-card, .big-tool-card, .quick-view-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.animation = 'fadeInUp 0.5s ease-out forwards';
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        observer.observe(card);
    });
}

// ============================================
// ENHANCED MODALS
// ============================================

function enhanceModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            this.style.animation = 'fadeIn 0.3s ease-out';
        });
        
        modal.addEventListener('hide.bs.modal', function() {
            this.style.animation = 'fadeOut 0.3s ease-out';
        });
    });
}

// ============================================
// NAVIGATION FLOW
// ============================================

function enhanceNavigation() {
    // Highlight active page in navigation
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Add page transition on navigation
    document.querySelectorAll('a:not([target="_blank"])').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href && !this.href.startsWith('#') && !this.href.includes('javascript:')) {
                const currentDomain = window.location.origin;
                if (this.href.startsWith(currentDomain)) {
                    // Same domain navigation - add transition
                    document.body.style.opacity = '0.8';
                }
            }
        });
    });
}

// ============================================
// QUICK SEARCH FUNCTIONALITY
// ============================================

function initializeQuickSearch() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    
    searchInputs.forEach(input => {
        // Add search icon
        const wrapper = document.createElement('div');
        wrapper.className = 'search-wrapper position-relative';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);
        
        const icon = document.createElement('i');
        icon.className = 'fas fa-search search-icon';
        icon.style.cssText = `
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: #6c757d;
            pointer-events: none;
        `;
        wrapper.appendChild(icon);
        
        input.style.paddingLeft = '2.5rem';
        
        // Live search indicator
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                icon.className = 'fas fa-spinner fa-spin search-icon';
                setTimeout(() => {
                    icon.className = 'fas fa-check search-icon';
                    icon.style.color = '#28a745';
                }, 500);
            } else {
                icon.className = 'fas fa-search search-icon';
                icon.style.color = '#6c757d';
            }
        });
    });
}

// ============================================
// ENHANCED TABLES
// ============================================

function enhanceTables() {
    document.querySelectorAll('.table tbody tr').forEach(row => {
        row.addEventListener('click', function(e) {
            // Don't trigger if clicking on button or link
            if (!e.target.closest('button, a')) {
                this.style.background = '#f8f9fa';
                setTimeout(() => {
                    this.style.background = '';
                }, 200);
            }
        });
    });
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.style.cssText = `
        position: fixed;
        top: 5rem;
        right: 1rem;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// ============================================
// LOADING OVERLAY
// ============================================

function showLoadingOverlay(message = 'Loading...') {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease-out;
    `;
    overlay.innerHTML = `
        <div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">${message}</p>
    `;
    
    document.body.appendChild(overlay);
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => overlay.remove(), 300);
    }
}

// ============================================
// ENHANCED CONFIRMATIONS
// ============================================

function confirmAction(message, callback) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="fas fa-exclamation-triangle me-2"></i>Confirm Action</h5>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger confirm-btn">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.querySelector('.confirm-btn').addEventListener('click', function() {
        callback();
        bsModal.hide();
        setTimeout(() => modal.remove(), 300);
    });
    
    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
    });
}

// ============================================
// DATA TABLE ENHANCEMENTS
// ============================================

function enhanceDataTables() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        // Add hover effect to rows
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.animationDelay = `${index * 50}ms`;
            row.style.animation = 'fadeInUp 0.5s ease-out forwards';
        });
        
        // Add sorting indicators (visual only)
        const headers = table.querySelectorAll('thead th');
        headers.forEach(header => {
            if (!header.querySelector('input, button')) {
                header.style.cursor = 'pointer';
                header.addEventListener('click', function() {
                    this.style.color = '#28a745';
                    setTimeout(() => {
                        this.style.color = '';
                    }, 300);
                });
            }
        });
    });
}

// ============================================
// PROGRESS TRACKING
// ============================================

function updateProgress(elementId, percentage) {
    const progressBar = document.getElementById(elementId);
    if (progressBar) {
        progressBar.style.width = '0%';
        setTimeout(() => {
            progressBar.style.width = percentage + '%';
            progressBar.style.transition = 'width 1s ease-out';
        }, 100);
    }
}

// ============================================
// BREADCRUMB AUTO-GENERATION
// ============================================

function generateBreadcrumbs() {
    const path = window.location.pathname;
    const parts = path.split('/').filter(p => p);
    
    if (parts.length > 1) {
        let breadcrumbHTML = '<nav aria-label="breadcrumb"><ol class="breadcrumb">';
        breadcrumbHTML += '<li class="breadcrumb-item"><a href="/"><i class="fas fa-home"></i> Home</a></li>';
        
        let currentPath = '';
        parts.forEach((part, index) => {
            currentPath += '/' + part;
            const isLast = index === parts.length - 1;
            const displayName = part.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            if (isLast) {
                breadcrumbHTML += `<li class="breadcrumb-item active">${displayName}</li>`;
            } else {
                breadcrumbHTML += `<li class="breadcrumb-item"><a href="${currentPath}">${displayName}</a></li>`;
            }
        });
        
        breadcrumbHTML += '</ol></nav>';
        
        const container = document.querySelector('.breadcrumb-container');
        if (container) {
            container.innerHTML = breadcrumbHTML;
        }
    }
}

// ============================================
// STATS COUNTER ANIMATION
// ============================================

function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

function animateAllCounters() {
    document.querySelectorAll('.stats-number').forEach(counter => {
        const target = parseInt(counter.textContent);
        if (!isNaN(target)) {
            counter.textContent = '0';
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(counter, target);
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(counter);
        }
    });
}

// ============================================
// SMART NAVIGATION FLOW
// ============================================

function createNavigationFlow() {
    // Add "Next Step" suggestions based on current page
    const currentPath = window.location.pathname;
    let nextStep = null;
    
    const flowMap = {
        '/': { next: '/signup/', text: 'Get Started - Sign Up' },
        '/signup/': { next: '/login/', text: 'Already have account? Login' },
        '/login/': { next: '/dashboard/', text: 'Go to Dashboard' },
        '/dashboard/': { next: '/ai-chatbot/chat/', text: 'Try AI Assistant' },
        '/ai-chatbot/chat/': { next: '/weather/', text: 'Check Weather' },
        '/weather/': { next: '/marketplace/', text: 'View Market Prices' },
        '/marketplace/': { next: '/schemes/', text: 'Explore Government Schemes' },
        '/schemes/': { next: '/problems/', text: 'Ask Expert' },
        '/problems/': { next: '/community/', text: 'Join Community' },
        '/admin-panel/': { next: '/admin-panel/users/', text: 'Manage Users' },
        '/admin-panel/users/': { next: '/admin-panel/content-moderation/', text: 'Moderate Content' },
    };
    
    if (flowMap[currentPath]) {
        const suggestion = document.createElement('div');
        suggestion.className = 'next-step-suggestion';
        suggestion.style.cssText = `
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            z-index: 998;
            animation: slideUp 0.5s ease-out;
        `;
        suggestion.innerHTML = `
            <span class="text-muted me-2">Next:</span>
            <a href="${flowMap[currentPath].next}" class="btn btn-sm btn-success">
                ${flowMap[currentPath].text} <i class="fas fa-arrow-right ms-2"></i>
            </a>
        `;
        
        document.body.appendChild(suggestion);
    }
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], input[name="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// ============================================
// INITIALIZE ON LOAD
// ============================================

window.addEventListener('load', function() {
    // Remove loading overlay if present
    hideLoadingOverlay();
    
    // Animate counters
    animateAllCounters();
    
    // Enhance data tables
    enhanceDataTables();
    
    // Initialize quick search
    initializeQuickSearch();
    
    // Create navigation flow
    createNavigationFlow();
    
    // Show success message for page load
    console.log('✅ Enhanced UX loaded successfully');
});

// ============================================
// EXPORT FUNCTIONS
// ============================================

window.FarmazeeUX = {
    showNotification,
    showLoadingOverlay,
    hideLoadingOverlay,
    confirmAction,
    updateProgress,
    animateCounter
};
