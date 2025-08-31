// Dynamic Settings Handler
class DynamicSettings {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme();
        this.createThemeToggle();
        this.applyDynamicStyles();
    }

    // Apply current theme
    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        document.body.setAttribute('data-theme', this.currentTheme);
    }

    // Toggle between light and dark themes
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.currentTheme);
        this.applyTheme();
        this.updateThemeToggleIcon();
    }

    // Create theme toggle button
    createThemeToggle() {
        if (!document.querySelector('.theme-toggle')) {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'theme-toggle';
            toggleBtn.innerHTML = this.getThemeToggleIcon();
            toggleBtn.addEventListener('click', () => this.toggleTheme());
            document.body.appendChild(toggleBtn);
        }
    }

    // Get appropriate icon for theme toggle
    getThemeToggleIcon() {
        return this.currentTheme === 'light' 
            ? '<i class="fas fa-moon"></i>' 
            : '<i class="fas fa-sun"></i>';
    }

    // Update theme toggle icon
    updateThemeToggleIcon() {
        const toggleBtn = document.querySelector('.theme-toggle');
        if (toggleBtn) {
            toggleBtn.innerHTML = this.getThemeToggleIcon();
        }
    }

    // Apply dynamic styles from system settings
    applyDynamicStyles() {
        // This would be populated from the backend with actual system settings
        const systemSettings = window.systemSettings || {};
        
        if (systemSettings.primary_color) {
            document.documentElement.style.setProperty('--primary-color', systemSettings.primary_color);
        }
        
        if (systemSettings.secondary_color) {
            document.documentElement.style.setProperty('--secondary-color', systemSettings.secondary_color);
        }
        
        if (systemSettings.accent_color) {
            document.documentElement.style.setProperty('--accent-color', systemSettings.accent_color);
        }
        
        if (systemSettings.font_family) {
            document.documentElement.style.setProperty('--font-family', systemSettings.font_family);
        }
    }

    // Update settings from admin panel
    updateSettings(newSettings) {
        Object.assign(window.systemSettings, newSettings);
        this.applyDynamicStyles();
        
        // Show success message
        this.showNotification('Settings updated successfully!', 'success');
    }

    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Feature toggle handler
    toggleFeature(featureName, enabled) {
        if (enabled) {
            document.body.classList.add(`feature-${featureName}-enabled`);
            document.body.classList.remove(`feature-${featureName}-disabled`);
        } else {
            document.body.classList.add(`feature-${featureName}-disabled`);
            document.body.classList.remove(`feature-${featureName}-enabled`);
        }
    }

    // Initialize feature toggles
    initFeatureToggles() {
        const features = [
            'marketplace', 'community', 'ai_chatbot', 'weather', 
            'soil_health', 'crop_planning', 'schemes'
        ];
        
        features.forEach(feature => {
            const isEnabled = window.systemSettings?.[`enable_${feature}`] !== false;
            this.toggleFeature(feature, isEnabled);
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dynamicSettings = new DynamicSettings();
    
    // Initialize feature toggles
    if (window.dynamicSettings) {
        window.dynamicSettings.initFeatureToggles();
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DynamicSettings;
}
