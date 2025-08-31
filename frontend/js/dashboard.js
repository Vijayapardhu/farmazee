/**
 * FARMazee - Dashboard JavaScript
 * Handles dashboard functionality and data management
 */

// Dashboard state
let dashboardData = {
    weather: null,
    crops: [],
    analytics: {},
    notifications: []
};

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('dashboard')) {
        initDashboard();
    }
});

/**
 * Initialize dashboard functionality
 */
function initDashboard() {
    loadDashboardData();
    initDashboardCharts();
    initDashboardWidgets();
    setupRealTimeUpdates();
}

/**
 * Load dashboard data from API
 */
async function loadDashboardData() {
    try {
        // Show loading state
        showDashboardLoading();
        
        // Load data in parallel
        const [weatherData, cropsData, analyticsData, notificationsData] = await Promise.all([
            loadWeatherData(),
            loadCropsData(),
            loadAnalyticsData(),
            loadNotificationsData()
        ]);
        
        // Update dashboard state
        dashboardData.weather = weatherData;
        dashboardData.crops = cropsData;
        dashboardData.analytics = analyticsData;
        dashboardData.notifications = notificationsData;
        
        // Render dashboard
        renderDashboard();
        
        // Hide loading state
        hideDashboardLoading();
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showDashboardError('Failed to load dashboard data. Please refresh the page.');
    }
}

/**
 * Load weather data
 */
async function loadWeatherData() {
    // Simulate API call (replace with actual API endpoint)
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
        current: {
            temperature: 24,
            humidity: 65,
            windSpeed: 12,
            condition: 'Partly Cloudy',
            icon: '🌤️'
        },
        forecast: [
            { day: 'Today', temp: 24, condition: '🌤️' },
            { day: 'Tomorrow', temp: 22, condition: '🌧️' },
            { day: 'Wed', temp: 26, condition: '☀️' },
            { day: 'Thu', temp: 25, condition: '🌤️' },
            { day: 'Fri', temp: 23, condition: '🌧️' }
        ],
        alerts: [
            { type: 'rain', message: 'Rain expected tomorrow', severity: 'moderate' }
        ]
    };
}

/**
 * Load crops data
 */
async function loadCropsData() {
    // Simulate API call (replace with actual API endpoint)
    await new Promise(resolve => setTimeout(resolve, 800));
    
    return [
        {
            id: 1,
            name: 'Wheat',
            variety: 'Durum',
            status: 'growing',
            plantedDate: '2025-01-15',
            expectedHarvest: '2025-05-20',
            health: 85,
            area: 2.5,
            progress: 65
        },
        {
            id: 2,
            name: 'Corn',
            variety: 'Sweet Corn',
            status: 'harvest-ready',
            plantedDate: '2025-01-10',
            expectedHarvest: '2025-04-25',
            health: 92,
            area: 1.8,
            progress: 95
        },
        {
            id: 3,
            name: 'Soybeans',
            variety: 'Roundup Ready',
            status: 'growing',
            plantedDate: '2025-02-01',
            expectedHarvest: '2025-06-15',
            health: 78,
            area: 3.2,
            progress: 45
        }
    ];
}

/**
 * Load analytics data
 */
async function loadAnalyticsData() {
    // Simulate API call (replace with actual API endpoint)
    await new Promise(resolve => setTimeout(resolve, 600));
    
    return {
        yield: {
            current: 28.5,
            previous: 25.2,
            change: 13.1,
            trend: 'up'
        },
        revenue: {
            current: 12500,
            previous: 11800,
            change: 5.9,
            trend: 'up'
        },
        expenses: {
            current: 8200,
            previous: 7800,
            change: 5.1,
            trend: 'up'
        },
        profit: {
            current: 4300,
            previous: 4000,
            change: 7.5,
            trend: 'up'
        }
    };
}

/**
 * Load notifications data
 */
async function loadNotificationsData() {
    // Simulate API call (replace with actual API endpoint)
    await new Promise(resolve => setTimeout(resolve, 400));
    
    return [
        {
            id: 1,
            type: 'weather',
            title: 'Weather Alert',
            message: 'Rain expected tomorrow. Consider delaying irrigation.',
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
            isRead: false,
            priority: 'high'
        },
        {
            id: 2,
            type: 'crop',
            title: 'Crop Monitoring',
            message: 'Corn field ready for harvest. Schedule harvesting equipment.',
            timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
            isRead: false,
            priority: 'medium'
        },
        {
            id: 3,
            type: 'soil',
            title: 'Soil Test Results',
            message: 'New soil test results available for wheat field.',
            timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
            isRead: true,
            priority: 'low'
        }
    ];
}

/**
 * Render dashboard with current data
 */
function renderDashboard() {
    renderWeatherWidget();
    renderCropsOverview();
    renderAnalyticsCharts();
    renderNotifications();
    renderQuickActions();
}

/**
 * Render weather widget
 */
function renderWeatherWidget() {
    const weatherWidget = document.querySelector('.weather-widget');
    if (!weatherWidget || !dashboardData.weather) return;
    
    const { current, forecast, alerts } = dashboardData.weather;
    
    weatherWidget.innerHTML = `
        <h3>Current Weather</h3>
        <div class="weather-info">
            <div class="weather-item">
                <div class="icon">${current.icon}</div>
                <div class="value">${current.temperature}°C</div>
                <div class="label">Temperature</div>
            </div>
            <div class="weather-item">
                <div class="icon">💧</div>
                <div class="value">${current.humidity}%</div>
                <div class="label">Humidity</div>
            </div>
            <div class="weather-item">
                <div class="icon">🌬️</div>
                <div class="value">${current.windSpeed} km/h</div>
                <div class="label">Wind Speed</div>
            </div>
        </div>
        
        ${alerts.length > 0 ? `
            <div class="weather-alerts">
                <h4>Weather Alerts</h4>
                ${alerts.map(alert => `
                    <div class="alert-item ${alert.severity}">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>${alert.message}</span>
                    </div>
                `).join('')}
            </div>
        ` : ''}
        
        <div class="weather-forecast">
            <h4>5-Day Forecast</h4>
            <div class="forecast-grid">
                ${forecast.map(day => `
                    <div class="forecast-day">
                        <div class="day">${day.day}</div>
                        <div class="icon">${day.condition}</div>
                        <div class="temp">${day.temp}°C</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

/**
 * Render crops overview
 */
function renderCropsOverview() {
    const cropsSection = document.querySelector('.crops-overview');
    if (!cropsSection) return;
    
    const { crops } = dashboardData;
    const totalArea = crops.reduce((sum, crop) => sum + crop.area, 0);
    const healthyCrops = crops.filter(crop => crop.health > 80).length;
    
    cropsSection.innerHTML = `
        <h3>Crops Overview</h3>
        <div class="crops-stats">
            <div class="stat-box">
                <span class="number">${crops.length}</span>
                <span class="label">Active Crops</span>
            </div>
            <div class="stat-box">
                <span class="number">${totalArea.toFixed(1)}</span>
                <span class="label">Total Area (ha)</span>
            </div>
            <div class="stat-box">
                <span class="number">${healthyCrops}</span>
                <span class="label">Healthy Crops</span>
            </div>
        </div>
        
        <div class="crops-list">
            ${crops.map(crop => `
                <div class="crop-item ${crop.status}">
                    <div class="crop-header">
                        <h4>${crop.name} - ${crop.variety}</h4>
                        <span class="crop-status ${crop.status}">${crop.status}</span>
                    </div>
                    <div class="crop-details">
                        <div class="crop-progress">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${crop.progress}%"></div>
                            </div>
                            <span>${crop.progress}% Complete</span>
                        </div>
                        <div class="crop-info">
                            <span>Health: ${crop.health}%</span>
                            <span>Area: ${crop.area} ha</span>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render analytics charts
 */
function renderAnalyticsCharts() {
    const analyticsSection = document.querySelector('.analytics-section');
    if (!analyticsSection || !dashboardData.analytics) return;
    
    const { yield, revenue, expenses, profit } = dashboardData.analytics;
    
    analyticsSection.innerHTML = `
        <h3>Financial Analytics</h3>
        <div class="analytics-grid">
            <div class="metric-card">
                <h4>Yield (tons)</h4>
                <div class="metric-value">${yield.current}</div>
                <div class="metric-change ${yield.trend}">
                    <i class="fas fa-arrow-${yield.trend === 'up' ? 'up' : 'down'}"></i>
                    ${yield.change}%
                </div>
            </div>
            <div class="metric-card">
                <h4>Revenue ($)</h4>
                <div class="metric-value">$${revenue.current.toLocaleString()}</div>
                <div class="metric-change ${revenue.trend}">
                    <i class="fas fa-arrow-${revenue.trend === 'up' ? 'up' : 'down'}"></i>
                    ${revenue.change}%
                </div>
            </div>
            <div class="metric-card">
                <h4>Expenses ($)</h4>
                <div class="metric-value">$${expenses.current.toLocaleString()}</div>
                <div class="metric-change ${expenses.trend}">
                    <i class="fas fa-arrow-${expenses.trend === 'up' ? 'up' : 'down'}"></i>
                    ${expenses.change}%
                </div>
            </div>
            <div class="metric-card">
                <h4>Profit ($)</h4>
                <div class="metric-value">$${profit.current.toLocaleString()}</div>
                <div class="metric-change ${profit.trend}">
                    <i class="fas fa-arrow-${profit.trend === 'up' ? 'up' : 'down'}"></i>
                    ${profit.change}%
                </div>
            </div>
        </div>
        
        <div class="chart-container">
            <canvas id="financialChart" width="400" height="200"></canvas>
        </div>
    `;
    
    // Initialize financial chart
    initFinancialChart();
}

/**
 * Render notifications
 */
function renderNotifications() {
    const notificationsSection = document.querySelector('.notifications-section');
    if (!notificationsSection) return;
    
    const { notifications } = dashboardData;
    const unreadCount = notifications.filter(n => !n.isRead).length;
    
    notificationsSection.innerHTML = `
        <h3>Notifications <span class="badge">${unreadCount}</span></h3>
        <div class="notifications-list">
            ${notifications.map(notification => `
                <div class="notification-item ${notification.isRead ? 'read' : 'unread'} ${notification.priority}">
                    <div class="notification-icon">
                        <i class="fas fa-${getNotificationIcon(notification.type)}"></i>
                    </div>
                    <div class="notification-content">
                        <h4>${notification.title}</h4>
                        <p>${notification.message}</p>
                        <span class="notification-time">${formatTimeAgo(notification.timestamp)}</span>
                    </div>
                    <div class="notification-actions">
                        <button class="btn-icon" onclick="markNotificationRead(${notification.id})">
                            <i class="fas fa-check"></i>
                        </button>
                        <button class="btn-icon" onclick="deleteNotification(${notification.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render quick actions
 */
function renderQuickActions() {
    const actionsSection = document.querySelector('.quick-actions');
    if (!actionsSection) return;
    
    actionsSection.innerHTML = `
        <h3>Quick Actions</h3>
        <div class="actions-grid">
            <button class="action-btn" onclick="addNewCrop()">
                <i class="fas fa-plus"></i>
                <span>Add New Crop</span>
            </button>
            <button class="action-btn" onclick="scheduleIrrigation()">
                <i class="fas fa-tint"></i>
                <span>Schedule Irrigation</span>
            </button>
            <button class="action-btn" onclick="bookEquipment()">
                <i class="fas fa-tractor"></i>
                <span>Book Equipment</span>
            </button>
            <button class="action-btn" onclick="contactExpert()">
                <i class="fas fa-user-tie"></i>
                <span>Contact Expert</span>
            </button>
        </div>
    `;
}

/**
 * Initialize dashboard charts
 */
function initDashboardCharts() {
    // This will be called when dashboard is loaded
    // Charts are initialized in renderAnalyticsCharts()
}

/**
 * Initialize financial chart
 */
function initFinancialChart() {
    const canvas = document.getElementById('financialChart');
    if (!canvas || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Revenue',
                data: [8000, 9500, 11000, 12500, 11800, 12500],
                borderColor: '#2E7D32',
                backgroundColor: 'rgba(46, 125, 50, 0.1)',
                tension: 0.4
            }, {
                label: 'Expenses',
                data: [6000, 6800, 7200, 7800, 7800, 8200],
                borderColor: '#FF9800',
                backgroundColor: 'rgba(255, 152, 0, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize dashboard widgets
 */
function initDashboardWidgets() {
    // Initialize any interactive widgets
    initWeatherAlerts();
    initCropProgressBars();
}

/**
 * Setup real-time updates
 */
function setupRealTimeUpdates() {
    // Update weather every 30 minutes
    setInterval(updateWeatherData, 30 * 60 * 1000);
    
    // Update notifications every 5 minutes
    setInterval(updateNotifications, 5 * 60 * 1000);
    
    // Update crop progress every hour
    setInterval(updateCropProgress, 60 * 60 * 1000);
}

/**
 * Show dashboard loading state
 */
function showDashboardLoading() {
    const dashboard = document.getElementById('dashboard');
    if (dashboard) {
        dashboard.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>Loading your farm data...</p>
            </div>
        `;
    }
}

/**
 * Hide dashboard loading state
 */
function hideDashboardLoading() {
    // Loading state is hidden when renderDashboard() is called
}

/**
 * Show dashboard error
 */
function showDashboardError(message) {
    const dashboard = document.getElementById('dashboard');
    if (dashboard) {
        dashboard.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Something went wrong</h3>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="loadDashboardData()">
                    <i class="fas fa-refresh"></i>
                    Try Again
                </button>
            </div>
        `;
    }
}

/**
 * Utility functions
 */
function getNotificationIcon(type) {
    const icons = {
        weather: 'cloud-rain',
        crop: 'seedling',
        soil: 'flask',
        equipment: 'tractor',
        market: 'store',
        default: 'bell'
    };
    return icons[type] || icons.default;
}

function formatTimeAgo(timestamp) {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
}

// Export functions for use in other modules
window.Dashboard = {
    initDashboard,
    loadDashboardData,
    renderDashboard,
    showDashboardLoading,
    hideDashboardLoading,
    showDashboardError
};

