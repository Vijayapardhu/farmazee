/**
 * FARMazee - Weather JavaScript
 * Handles weather forecasting and alerts
 */

// Weather state
let weatherData = {
    current: null,
    forecast: [],
    alerts: [],
    location: null
};

// Initialize weather functionality
document.addEventListener('DOMContentLoaded', function() {
    initWeather();
});

/**
 * Initialize weather functionality
 */
function initWeather() {
    getCurrentLocation();
    loadWeatherData();
    setupWeatherUpdates();
}

/**
 * Get current location
 */
function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                weatherData.location = {
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                };
                loadWeatherData();
            },
            error => {
                console.error('Error getting location:', error);
                // Use default location
                weatherData.location = { lat: 20.5937, lon: 78.9629 }; // India
                loadWeatherData();
            }
        );
    } else {
        // Use default location
        weatherData.location = { lat: 20.5937, lon: 78.9629 }; // India
        loadWeatherData();
    }
}

/**
 * Load weather data
 */
async function loadWeatherData() {
    try {
        const data = await fetchWeatherData();
        weatherData.current = data.current;
        weatherData.forecast = data.forecast;
        weatherData.alerts = data.alerts;
        
        renderWeatherData();
        checkWeatherAlerts();
        
    } catch (error) {
        console.error('Error loading weather data:', error);
        showWeatherError('Failed to load weather data');
    }
}

/**
 * Fetch weather data from API
 */
async function fetchWeatherData() {
    // Simulate API call (replace with actual OpenWeatherMap API)
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
        current: {
            temperature: 24,
            feels_like: 26,
            humidity: 65,
            wind_speed: 12,
            wind_direction: 180,
            pressure: 1013,
            visibility: 10,
            condition: 'Partly Cloudy',
            icon: '🌤️',
            uv_index: 6
        },
        forecast: [
            {
                date: '2025-01-30',
                temp_min: 18,
                temp_max: 26,
                condition: 'Partly Cloudy',
                icon: '🌤️',
                humidity: 70,
                wind_speed: 10
            },
            {
                date: '2025-01-31',
                temp_min: 16,
                temp_max: 22,
                condition: 'Rain',
                icon: '🌧️',
                humidity: 85,
                wind_speed: 15
            },
            {
                date: '2025-02-01',
                temp_min: 20,
                temp_max: 28,
                condition: 'Sunny',
                icon: '☀️',
                humidity: 55,
                wind_speed: 8
            }
        ],
        alerts: [
            {
                type: 'rain',
                severity: 'moderate',
                title: 'Rain Expected',
                description: 'Moderate rainfall expected tomorrow. Consider delaying irrigation.',
                start: '2025-01-31T06:00:00',
                end: '2025-01-31T18:00:00'
            }
        ]
    };
}

/**
 * Render weather data
 */
function renderWeatherData() {
    renderCurrentWeather();
    renderWeatherForecast();
    renderWeatherAlerts();
    renderWeatherMap();
}

/**
 * Render current weather
 */
function renderCurrentWeather() {
    const container = document.querySelector('.current-weather');
    if (!container || !weatherData.current) return;
    
    const current = weatherData.current;
    
    container.innerHTML = `
        <div class="weather-main">
            <div class="weather-icon">${current.icon}</div>
            <div class="weather-temp">
                <span class="temp-value">${current.temperature}°C</span>
                <span class="temp-feels">Feels like ${current.feels_like}°C</span>
            </div>
        </div>
        <div class="weather-details">
            <div class="weather-detail">
                <i class="fas fa-tint"></i>
                <span>Humidity: ${current.humidity}%</span>
            </div>
            <div class="weather-detail">
                <i class="fas fa-wind"></i>
                <span>Wind: ${current.wind_speed} km/h</span>
            </div>
            <div class="weather-detail">
                <i class="fas fa-compress-alt"></i>
                <span>Pressure: ${current.pressure} hPa</span>
            </div>
            <div class="weather-detail">
                <i class="fas fa-eye"></i>
                <span>Visibility: ${current.visibility} km</span>
            </div>
        </div>
    `;
}

/**
 * Render weather forecast
 */
function renderWeatherForecast() {
    const container = document.querySelector('.weather-forecast');
    if (!container || !weatherData.forecast) return;
    
    container.innerHTML = `
        <h3>3-Day Forecast</h3>
        <div class="forecast-grid">
            ${weatherData.forecast.map(day => `
                <div class="forecast-day">
                    <div class="forecast-date">${formatDate(day.date)}</div>
                    <div class="forecast-icon">${day.icon}</div>
                    <div class="forecast-temp">
                        <span class="temp-max">${day.temp_max}°</span>
                        <span class="temp-min">${day.temp_min}°</span>
                    </div>
                    <div class="forecast-condition">${day.condition}</div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render weather alerts
 */
function renderWeatherAlerts() {
    const container = document.querySelector('.weather-alerts');
    if (!container) return;
    
    if (weatherData.alerts.length === 0) {
        container.innerHTML = `
            <h3>Weather Alerts</h3>
            <p class="no-alerts">No weather alerts at this time.</p>
        `;
        return;
    }
    
    container.innerHTML = `
        <h3>Weather Alerts</h3>
        <div class="alerts-list">
            ${weatherData.alerts.map(alert => `
                <div class="alert-item ${alert.severity}">
                    <div class="alert-header">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span class="alert-title">${alert.title}</span>
                        <span class="alert-severity">${alert.severity}</span>
                    </div>
                    <p class="alert-description">${alert.description}</p>
                    <div class="alert-time">
                        <span>From: ${formatDateTime(alert.start)}</span>
                        <span>To: ${formatDateTime(alert.end)}</span>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render weather map
 */
function renderWeatherMap() {
    const container = document.querySelector('.weather-map');
    if (!container || !weatherData.location) return;
    
    container.innerHTML = `
        <h3>Weather Map</h3>
        <div id="map" style="height: 300px; width: 100%;"></div>
    `;
    
    // Initialize map (requires Leaflet)
    initWeatherMap();
}

/**
 * Initialize weather map
 */
function initWeatherMap() {
    if (typeof L === 'undefined') return;
    
    const map = L.map('map').setView([weatherData.location.lat, weatherData.location.lon], 10);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Add weather overlay (requires weather tile service)
    // L.tileLayer('https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={api_key}', {
    //     layer: 'temp_new',
    //     api_key: 'your_api_key'
    // }).addTo(map);
    
    // Add marker for current location
    L.marker([weatherData.location.lat, weatherData.location.lon])
        .addTo(map)
        .bindPopup('Your Location')
        .openPopup();
}

/**
 * Check weather alerts
 */
function checkWeatherAlerts() {
    if (weatherData.alerts.length === 0) return;
    
    weatherData.alerts.forEach(alert => {
        if (alert.severity === 'high' || alert.severity === 'extreme') {
            showWeatherAlert(alert);
        }
    });
}

/**
 * Show weather alert notification
 */
function showWeatherAlert(alert) {
    const notification = document.createElement('div');
    notification.className = `weather-alert-notification ${alert.severity}`;
    notification.innerHTML = `
        <div class="alert-content">
            <i class="fas fa-exclamation-triangle"></i>
            <div class="alert-text">
                <h4>${alert.title}</h4>
                <p>${alert.description}</p>
            </div>
            <button class="alert-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 10 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 10000);
}

/**
 * Setup weather updates
 */
function setupWeatherUpdates() {
    // Update weather every 30 minutes
    setInterval(loadWeatherData, 30 * 60 * 1000);
    
    // Check for new alerts every 5 minutes
    setInterval(checkForNewAlerts, 5 * 60 * 1000);
}

/**
 * Check for new weather alerts
 */
async function checkForNewAlerts() {
    try {
        const newData = await fetchWeatherData();
        const newAlerts = newData.alerts.filter(alert => 
            !weatherData.alerts.some(existing => 
                existing.start === alert.start && existing.end === alert.end
            )
        );
        
        if (newAlerts.length > 0) {
            weatherData.alerts = newData.alerts;
            renderWeatherAlerts();
            newAlerts.forEach(alert => showWeatherAlert(alert));
        }
    } catch (error) {
        console.error('Error checking for new alerts:', error);
    }
}

/**
 * Show weather error
 */
function showWeatherError(message) {
    const container = document.querySelector('.weather-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="weather-error">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Weather Data Unavailable</h3>
            <p>${message}</p>
            <button class="btn btn-primary" onclick="loadWeatherData()">
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
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
    });
}

function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Export functions for use in other modules
window.Weather = {
    initWeather,
    loadWeatherData,
    renderWeatherData,
    checkWeatherAlerts,
    showWeatherAlert
};

