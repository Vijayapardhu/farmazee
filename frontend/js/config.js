// Farmazee Configuration
// Central configuration file for all settings and branding

const FarmazeeConfig = {
    // Brand Information
    brand: {
        name: 'Farmazee',
        tagline: 'Smart Farming Platform for Modern Agriculture',
        description: 'Empowering farmers with cutting-edge AI technology, real-time weather insights, and expert agricultural knowledge to achieve better yields and sustainable farming practices.',
        website: 'https://farmazee.com',
        email: 'info@farmazee.com',
        phone: '+1 (555) 123-4567',
        address: '123 Farming Street, Agriculture City, AC 12345'
    },

    // API Configuration
    api: {
        baseURL: 'http://localhost:8000/api',
        version: 'v1',
        timeout: 30000, // 30 seconds
        retryAttempts: 3,
        retryDelay: 1000, // 1 second
        endpoints: {
            auth: {
                login: '/auth/login/',
                signup: '/auth/signup/',
                logout: '/auth/logout/',
                refresh: '/auth/refresh/'
            },
            users: {
                profile: '/users/profile/',
                update: '/users/profile/'
            },
            weather: {
                current: '/weather/current/',
                forecast: '/weather/forecast/',
                alerts: '/weather/alerts/'
            },
            crops: {
                list: '/crops/',
                create: '/crops/',
                update: '/crops/{id}/',
                delete: '/crops/{id}/'
            },
            marketplace: {
                products: '/marketplace/products/',
                create: '/marketplace/products/',
                categories: '/marketplace/categories/'
            },
            community: {
                topics: '/community/topics/',
                questions: '/community/questions/',
                experts: '/community/experts/',
                events: '/community/events/'
            },
            schemes: {
                list: '/schemes/',
                apply: '/schemes/{id}/apply/',
                categories: '/schemes/categories/'
            },
            soil: {
                tests: '/soil/tests/',
                recommendations: '/soil/recommendations/',
                monitoring: '/soil/monitoring/',
                types: '/soil/types/',
                nutrients: '/soil/nutrients/'
            }
        }
    },

    // Feature Flags
    features: {
        weather: true,
        crops: true,
        marketplace: true,
        community: true,
        schemes: true,
        soilHealth: true,
        aiRecommendations: true,
        mobileApp: false,
        offlineMode: false,
        multiLanguage: true
    },

    // External Services
    external: {
        weatherAPI: {
            provider: 'OpenWeatherMap',
            baseURL: 'https://api.openweathermap.org/data/2.5',
            apiKey: 'YOUR_OPENWEATHER_API_KEY'
        },
        maps: {
            provider: 'Leaflet',
            tileLayer: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution: '© OpenStreetMap contributors'
        },
        analytics: {
            googleAnalytics: 'GA_MEASUREMENT_ID',
            facebookPixel: 'FB_PIXEL_ID'
        }
    },

    // UI Configuration
    ui: {
        theme: {
            primary: '#2E7D32',
            secondary: '#FF9800',
            accent: '#FFD700',
            success: '#4CAF50',
            warning: '#FF9800',
            error: '#F44336',
            info: '#2196F3'
        },
        animations: {
            enabled: true,
            duration: 300,
            easing: 'ease-in-out'
        },
        responsive: {
            breakpoints: {
                mobile: 768,
                tablet: 1024,
                desktop: 1200
            }
        }
    },

    // Localization
    localization: {
        defaultLanguage: 'en',
        supportedLanguages: ['en', 'te', 'hi'],
        translations: {
            en: {
                name: 'English',
                flag: '🇺🇸'
            },
            te: {
                name: 'తెలుగు',
                flag: '🇮🇳'
            },
            hi: {
                name: 'हिंदी',
                flag: '🇮🇳'
            }
        }
    },

    // Constants
    constants: {
        maxFileSize: 5 * 1024 * 1024, // 5MB
        supportedImageFormats: ['jpg', 'jpeg', 'png', 'gif', 'webp'],
        maxUploads: 10,
        sessionTimeout: 24 * 60 * 60 * 1000, // 24 hours
        refreshTokenExpiry: 7 * 24 * 60 * 60 * 1000 // 7 days
    },

    // Development Settings
    development: {
        debug: true,
        logLevel: 'info',
        mockData: false,
        apiMocking: false
    },

    // Production Settings
    production: {
        debug: false,
        logLevel: 'error',
        mockData: false,
        apiMocking: false
    }
};

// Environment-specific configuration
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname.includes('dev');

const config = isDevelopment ? 
    { ...FarmazeeConfig, ...FarmazeeConfig.development } : 
    { ...FarmazeeConfig, ...FarmazeeConfig.production };

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
} else {
    window.FarmazeeConfig = config;
}

// Log configuration status
console.log(`Farmazee Config Loaded - Environment: ${isDevelopment ? 'Development' : 'Production'}`);
console.log('API Base URL:', config.api.baseURL);
console.log('Features Enabled:', Object.keys(config.features).filter(key => config.features[key]));
