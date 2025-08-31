/**
 * FARMazee - Main JavaScript
 * Core functionality and utilities
 */

// Global variables
let currentUser = null;
let isAuthenticated = false;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Hide loading screen
    hideLoadingScreen();
    
    // Initialize navigation
    initNavigation();
    
    // Initialize smooth scrolling
    initSmoothScrolling();
    
    // Initialize animations
    initAnimations();
    
    // Initialize contact form
    initContactForm();
    
    // Check authentication status
    checkAuthStatus();
    
    // Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100
        });
    }
}

/**
 * Hide loading screen with animation
 */
function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }, 1000);
    }
}

/**
 * Initialize navigation functionality
 */
function initNavigation() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile navigation toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navToggle && navMenu) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navbar.contains(e.target)) {
            if (navToggle && navMenu) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        }
    });
    
    // Active navigation highlighting
    updateActiveNavLink();
    window.addEventListener('scroll', updateActiveNavLink);
}

/**
 * Update active navigation link based on scroll position
 */
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Initialize animations and effects
 */
function initAnimations() {
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Counter animation for stats
    const statNumbers = document.querySelectorAll('.stat-item h3');
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalNumber = parseInt(target.textContent);
                animateCounter(target, 0, finalNumber, 2000);
                observer.unobserve(target);
            }
        });
    }, observerOptions);
    
    statNumbers.forEach(stat => observer.observe(stat));
}

/**
 * Animate counter from start to end value
 */
function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current + (end >= 1000 ? '+' : '');
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

/**
 * Initialize contact form
 */
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }
}

/**
 * Handle contact form submission
 */
async function handleContactSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    try {
        // Show loading state
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        
        // Simulate API call (replace with actual API endpoint)
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Show success message
        showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
        
        // Reset form
        e.target.reset();
        
    } catch (error) {
        showNotification('Failed to send message. Please try again.', 'error');
    } finally {
        // Reset button state
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

/**
 * Check authentication status
 */
function checkAuthStatus() {
    const token = localStorage.getItem('farmazee_token');
    if (token) {
        // Validate token (replace with actual validation)
        isAuthenticated = true;
        currentUser = JSON.parse(localStorage.getItem('farmazee_user') || '{}');
        updateUIForAuthenticatedUser();
    } else {
        updateUIForUnauthenticatedUser();
    }
}

/**
 * Update UI for authenticated users
 */
function updateUIForAuthenticatedUser() {
    const loginLink = document.getElementById('login-link');
    const signupLink = document.getElementById('signup-link');
    
    if (loginLink && signupLink) {
        loginLink.textContent = 'Dashboard';
        loginLink.href = '#dashboard';
        loginLink.onclick = () => showDashboard();
        
        signupLink.textContent = 'Logout';
        signupLink.href = '#';
        signupLink.onclick = logout;
        signupLink.classList.remove('btn-primary');
        signupLink.classList.add('btn-secondary');
    }
}

/**
 * Update UI for unauthenticated users
 */
function updateUIForUnauthenticatedUser() {
    const loginLink = document.getElementById('login-link');
    const signupLink = document.getElementById('signup-link');
    
    if (loginLink && signupLink) {
        loginLink.textContent = 'Login';
        loginLink.href = '#login';
        loginLink.onclick = showLoginModal;
        
        signupLink.textContent = 'Sign Up';
        signupLink.href = '#signup';
        signupLink.onclick = showSignupModal;
        signupLink.classList.remove('btn-secondary');
        signupLink.classList.add('btn-primary');
    }
}

/**
 * Show dashboard
 */
function showDashboard() {
    if (!isAuthenticated) {
        showLoginModal();
        return;
    }
    
    // Hide main content
    const mainContent = document.getElementById('main-content');
    const dashboard = document.getElementById('dashboard');
    
    if (mainContent && dashboard) {
        mainContent.style.display = 'none';
        dashboard.style.display = 'block';
        
        // Load dashboard content
        loadDashboardContent();
    }
}

/**
 * Load dashboard content
 */
function loadDashboardContent() {
    const dashboard = document.getElementById('dashboard');
    if (!dashboard) return;
    
    dashboard.innerHTML = `
        <div class="dashboard-header">
            <div class="container">
                <h1>Welcome back, ${currentUser?.name || 'Farmer'}!</h1>
                <p>Here's what's happening on your farm today</p>
            </div>
        </div>
        
        <div class="container">
            <div class="dashboard-grid">
                <div class="dashboard-card">
                    <h3><i class="fas fa-cloud-sun"></i> Weather</h3>
                    <div class="weather-widget">
                        <h3>Current Weather</h3>
                        <div class="weather-info">
                            <div class="weather-item">
                                <div class="icon">🌤️</div>
                                <div class="value">24°C</div>
                                <div class="label">Temperature</div>
                            </div>
                            <div class="weather-item">
                                <div class="icon">💧</div>
                                <div class="value">65%</div>
                                <div class="label">Humidity</div>
                            </div>
                            <div class="weather-item">
                                <div class="icon">🌬️</div>
                                <div class="value">12 km/h</div>
                                <div class="label">Wind Speed</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <h3><i class="fas fa-seedling"></i> Crops</h3>
                    <div class="dashboard-stats">
                        <div class="stat-box">
                            <span class="number">5</span>
                            <span class="label">Active Crops</span>
                        </div>
                        <div class="stat-box">
                            <span class="number">2</span>
                            <span class="label">Ready to Harvest</span>
                        </div>
                        <div class="stat-box">
                            <span class="number">3</span>
                            <span class="label">Growing</span>
                        </div>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <h3><i class="fas fa-chart-line"></i> Analytics</h3>
                    <div class="chart-container">
                        <div class="chart-header">
                            <h4 class="chart-title">Yield Trends</h4>
                            <div class="chart-controls">
                                <button class="chart-control active">Week</button>
                                <button class="chart-control">Month</button>
                                <button class="chart-control">Year</button>
                            </div>
                        </div>
                        <canvas id="yieldChart" width="400" height="200"></canvas>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <h3><i class="fas fa-bell"></i> Notifications</h3>
                    <div class="notification-list">
                        <div class="notification-item">
                            <i class="fas fa-info-circle text-info"></i>
                            <span>Weather alert: Rain expected tomorrow</span>
                        </div>
                        <div class="notification-item">
                            <i class="fas fa-check-circle text-success"></i>
                            <span>Crop monitoring scheduled for today</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Initialize charts
    initDashboardCharts();
}

/**
 * Initialize dashboard charts
 */
function initDashboardCharts() {
    const canvas = document.getElementById('yieldChart');
    if (!canvas || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Yield (tons)',
                data: [12, 19, 15, 25, 22, 30, 28],
                borderColor: '#2E7D32',
                backgroundColor: 'rgba(46, 125, 50, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * Logout function
 */
function logout() {
    localStorage.removeItem('farmazee_token');
    localStorage.removeItem('farmazee_user');
    isAuthenticated = false;
    currentUser = null;
    
    updateUIForUnauthenticatedUser();
    
    // Show main content
    const mainContent = document.getElementById('main-content');
    const dashboard = document.getElementById('dashboard');
    
    if (mainContent && dashboard) {
        mainContent.style.display = 'block';
        dashboard.style.display = 'none';
    }
    
    showNotification('Logged out successfully', 'success');
}

/**
 * Utility function to scroll to section
 */
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offsetTop = section.offsetTop - 80;
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

/**
 * Open demo video
 */
function openDemo() {
    showNotification('Demo video feature coming soon!', 'info');
}

/**
 * Show login modal
 */
function showLoginModal() {
    const modal = document.getElementById('login-modal');
    if (modal) {
        modal.style.display = 'block';
    }
}

/**
 * Show signup modal
 */
function showSignupModal() {
    const modal = document.getElementById('signup-modal');
    if (modal) {
        modal.style.display = 'block';
    }
}

// Export functions for use in other modules
window.Farmazee = {
    showNotification,
    scrollToSection,
    showDashboard,
    logout,
    showLoginModal,
    showSignupModal
};

/**
 * Initialize tab functionality for community and soil health sections
 */
function initializeTabs() {
    // Community tabs
    const communityTabs = document.querySelectorAll('.community-tabs .tab-btn');
    const communityContents = document.querySelectorAll('.community-section .tab-content');
    
    communityTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            communityTabs.forEach(t => t.classList.remove('active'));
            communityContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
    
    // Soil health tabs
    const soilTabs = document.querySelectorAll('.soil-health-tabs .tab-btn');
    const soilContents = document.querySelectorAll('.soil-health-section .tab-content');
    
    soilTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            soilTabs.forEach(t => t.classList.remove('active'));
            soilContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

// Initialize tabs when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
});
