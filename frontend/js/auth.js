/**
 * FARMazee - Authentication JavaScript
 * Handles login, signup, and user authentication
 */

// Modal functionality
document.addEventListener('DOMContentLoaded', function() {
    initAuthModals();
});

/**
 * Initialize authentication modals
 */
function initAuthModals() {
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close');
    
    // Close modal when clicking on close button
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Close modal when clicking outside
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.style.display = 'none';
            }
        });
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            modals.forEach(modal => {
                if (modal.style.display === 'block') {
                    modal.style.display = 'none';
                }
            });
        }
    });
    
    // Initialize forms
    initLoginForm();
    initSignupForm();
}

/**
 * Initialize login form
 */
function initLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
}

/**
 * Initialize signup form
 */
function initSignupForm() {
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
}

/**
 * Handle login form submission
 */
async function handleLogin(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const email = formData.get('email') || document.getElementById('login-email').value;
    const password = formData.get('password') || document.getElementById('login-password').value;
    
    if (!email || !password) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    try {
        // Show loading state
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
        
        // Simulate API call (replace with actual API endpoint)
        const response = await simulateLoginAPI(email, password);
        
        if (response.success) {
            // Store authentication data
            localStorage.setItem('farmazee_token', response.token);
            localStorage.setItem('farmazee_user', JSON.stringify(response.user));
            
            // Update global state
            window.isAuthenticated = true;
            window.currentUser = response.user;
            
            // Show success message
            showNotification('Login successful! Welcome back.', 'success');
            
            // Close modal
            const modal = document.getElementById('login-modal');
            if (modal) {
                modal.style.display = 'none';
            }
            
            // Update UI
            updateUIForAuthenticatedUser();
            
            // Redirect to dashboard
            setTimeout(() => {
                showDashboard();
            }, 1000);
            
        } else {
            showNotification(response.message || 'Login failed. Please check your credentials.', 'error');
        }
        
    } catch (error) {
        console.error('Login error:', error);
        showNotification('An error occurred during login. Please try again.', 'error');
    } finally {
        // Reset button state
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

/**
 * Handle signup form submission
 */
async function handleSignup(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const name = formData.get('name') || document.getElementById('signup-name').value;
    const email = formData.get('email') || document.getElementById('signup-email').value;
    const password = formData.get('password') || document.getElementById('signup-password').value;
    const confirmPassword = formData.get('confirm-password') || document.getElementById('signup-confirm-password').value;
    
    // Validation
    if (!name || !email || !password || !confirmPassword) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }
    
    if (password.length < 6) {
        showNotification('Password must be at least 6 characters long', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    try {
        // Show loading state
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account...';
        
        // Simulate API call (replace with actual API endpoint)
        const response = await simulateSignupAPI(name, email, password);
        
        if (response.success) {
            // Store authentication data
            localStorage.setItem('farmazee_token', response.token);
            localStorage.setItem('farmazee_user', JSON.stringify(response.user));
            
            // Update global state
            window.isAuthenticated = true;
            window.currentUser = response.user;
            
            // Show success message
            showNotification('Account created successfully! Welcome to Farmazee.', 'success');
            
            // Close modal
            const modal = document.getElementById('signup-modal');
            if (modal) {
                modal.style.display = 'none';
            }
            
            // Update UI
            updateUIForAuthenticatedUser();
            
            // Redirect to dashboard
            setTimeout(() => {
                showDashboard();
            }, 1000);
            
        } else {
            showNotification(response.message || 'Signup failed. Please try again.', 'error');
        }
        
    } catch (error) {
        console.error('Signup error:', error);
        showNotification('An error occurred during signup. Please try again.', 'error');
    } finally {
        // Reset button state
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

/**
 * Simulate login API call
 */
async function simulateLoginAPI(email, password) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock validation (replace with actual API call)
    if (email === 'demo@farmazee.com' && password === 'demo123') {
        return {
            success: true,
            token: 'mock_jwt_token_' + Date.now(),
            user: {
                id: 1,
                name: 'Demo Farmer',
                email: 'demo@farmazee.com',
                role: 'farmer',
                farm_type: 'mixed',
                experience_years: 5
            }
        };
    } else if (email === 'admin@farmazee.com' && password === 'admin123') {
        return {
            success: true,
            token: 'mock_admin_token_' + Date.now(),
            user: {
                id: 2,
                name: 'Admin User',
                email: 'admin@farmazee.com',
                role: 'admin',
                farm_type: 'none',
                experience_years: 0
            }
        };
    } else {
        return {
            success: false,
            message: 'Invalid email or password'
        };
    }
}

/**
 * Simulate signup API call
 */
async function simulateSignupAPI(name, email, password) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock validation (replace with actual API call)
    if (email === 'existing@farmazee.com') {
        return {
            success: false,
            message: 'Email already exists. Please use a different email or try logging in.'
        };
    }
    
    return {
        success: true,
        token: 'mock_jwt_token_' + Date.now(),
        user: {
            id: Date.now(),
            name: name,
            email: email,
            role: 'farmer',
            farm_type: 'mixed',
            experience_years: 0
        }
    };
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show login modal
 */
function showLoginModal() {
    const modal = document.getElementById('login-modal');
    if (modal) {
        modal.style.display = 'block';
        // Focus on first input
        const firstInput = modal.querySelector('input');
        if (firstInput) {
            firstInput.focus();
        }
    }
}

/**
 * Show signup modal
 */
function showSignupModal() {
    const modal = document.getElementById('signup-modal');
    if (modal) {
        modal.style.display = 'block';
        // Focus on first input
        const firstInput = modal.querySelector('input');
        if (firstInput) {
            firstInput.focus();
        }
    }
}

/**
 * Switch between login and signup modals
 */
function switchToSignup() {
    const loginModal = document.getElementById('login-modal');
    const signupModal = document.getElementById('signup-modal');
    
    if (loginModal && signupModal) {
        loginModal.style.display = 'none';
        signupModal.style.display = 'block';
        
        // Focus on first input
        const firstInput = signupModal.querySelector('input');
        if (firstInput) {
            firstInput.focus();
        }
    }
}

function switchToLogin() {
    const loginModal = document.getElementById('login-modal');
    const signupModal = document.getElementById('signup-modal');
    
    if (loginModal && signupModal) {
        signupModal.style.display = 'none';
        loginModal.style.display = 'block';
        
        // Focus on first input
        const firstInput = loginModal.querySelector('input');
        if (firstInput) {
            firstInput.focus();
        }
    }
}

/**
 * Logout user
 */
function logout() {
    // Clear authentication data
    localStorage.removeItem('farmazee_token');
    localStorage.removeItem('farmazee_user');
    
    // Update global state
    window.isAuthenticated = false;
    window.currentUser = null;
    
    // Update UI
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
 * Check if user is authenticated
 */
function isAuthenticated() {
    const token = localStorage.getItem('farmazee_token');
    return !!token;
}

/**
 * Get current user data
 */
function getCurrentUser() {
    const userData = localStorage.getItem('farmazee_user');
    return userData ? JSON.parse(userData) : null;
}

/**
 * Get authentication token
 */
function getAuthToken() {
    return localStorage.getItem('farmazee_token');
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
 * Show dashboard (placeholder - implement in main.js)
 */
function showDashboard() {
    // This function should be implemented in main.js
    if (window.Farmazee && window.Farmazee.showDashboard) {
        window.Farmazee.showDashboard();
    } else {
        showNotification('Dashboard feature coming soon!', 'info');
    }
}

/**
 * Show notification (placeholder - implement in main.js)
 */
function showNotification(message, type = 'info') {
    // This function should be implemented in main.js
    if (window.Farmazee && window.Farmazee.showNotification) {
        window.Farmazee.showNotification(message, type);
    } else {
        // Fallback notification
        alert(`${type.toUpperCase()}: ${message}`);
    }
}

// Export functions for use in other modules
window.Auth = {
    showLoginModal,
    showSignupModal,
    switchToSignup,
    switchToLogin,
    logout,
    isAuthenticated,
    getCurrentUser,
    getAuthToken,
    updateUIForAuthenticatedUser,
    updateUIForUnauthenticatedUser
};

