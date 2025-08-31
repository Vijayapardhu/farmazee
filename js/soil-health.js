// Soil Health Management for Farmazee
class SoilHealthManager {
    constructor() {
        this.soilHealthData = {
            soilTests: [],
            soilTypes: [],
            recommendations: [],
            monitoringData: [],
            alerts: []
        };
        this.currentUser = null;
        this.isInitialized = false;
    }

    init() {
        if (this.isInitialized) return;
        this.currentUser = this.getCurrentUser();
        this.loadSoilHealthData();
        this.setupEventListeners();
        this.isInitialized = true;
        console.log('Soil Health Manager initialized');
    }

    getCurrentUser() {
        const userStr = localStorage.getItem('farmazee_user');
        return userStr ? JSON.parse(userStr) : null;
    }

    async loadSoilHealthData() {
        try {
            await Promise.all([
                this.loadSoilTests(),
                this.loadSoilTypes(),
                this.loadRecommendations(),
                this.loadMonitoringData(),
                this.loadAlerts()
            ]);
            this.renderSoilHealthData();
        } catch (error) {
            console.error('Error loading soil health data:', error);
            this.showSoilHealthError('Failed to load soil health data');
        }
    }

    async loadSoilTests() {
        this.soilHealthData.soilTests = [
            {
                id: 1,
                testDate: '2025-01-15T10:00:00Z',
                location: 'Field A - North Section',
                soilDepth: '0-30 cm',
                phLevel: 6.8,
                organicMatter: 2.1,
                nitrogen: 45,
                phosphorus: 28,
                potassium: 180,
                status: 'Completed',
                recommendations: 'Good soil health, maintain current practices'
            },
            {
                id: 2,
                testDate: '2025-01-10T14:30:00Z',
                location: 'Field B - South Section',
                soilDepth: '0-30 cm',
                phLevel: 5.2,
                organicMatter: 1.3,
                nitrogen: 32,
                phosphorus: 15,
                potassium: 120,
                status: 'Completed',
                recommendations: 'Low pH and phosphorus, apply lime and phosphate fertilizers'
            }
        ];
    }

    async loadSoilTypes() {
        this.soilHealthData.soilTypes = [
            {
                id: 1,
                name: 'Clay Loam',
                description: 'Good water retention, suitable for most crops',
                characteristics: 'High fertility, good structure',
                suitableCrops: ['Rice', 'Wheat', 'Cotton', 'Vegetables'],
                image: './assets/images/soil-clay-loam.jpg'
            },
            {
                id: 2,
                name: 'Sandy Loam',
                description: 'Well-draining, warms quickly in spring',
                characteristics: 'Easy to work, good aeration',
                suitableCrops: ['Groundnuts', 'Pulses', 'Vegetables'],
                image: './assets/images/soil-sandy-loam.jpg'
            }
        ];
    }

    async loadRecommendations() {
        this.soilHealthData.recommendations = [
            {
                id: 1,
                type: 'Fertilizer',
                title: 'Phosphorus Application',
                description: 'Apply DAP or SSP at 50 kg per acre',
                applicationRate: '50 kg/acre',
                applicationMethod: 'Broadcast before sowing',
                timing: 'Pre-sowing',
                precautions: 'Avoid direct contact with seeds'
            },
            {
                id: 2,
                type: 'Soil Amendment',
                title: 'Lime Application',
                description: 'Apply agricultural lime to raise pH',
                applicationRate: '500 kg/acre',
                applicationMethod: 'Broadcast and incorporate',
                timing: '2-3 weeks before sowing',
                precautions: 'Test soil pH after 3 months'
            }
        ];
    }

    async loadMonitoringData() {
        this.soilHealthData.monitoringData = [
            {
                id: 1,
                date: '2025-01-15T08:00:00Z',
                location: 'Field A',
                moistureLevel: 65,
                temperature: 24,
                humidity: 78,
                rainfall: 0,
                notes: 'Optimal moisture for crop growth'
            },
            {
                id: 2,
                date: '2025-01-14T08:00:00Z',
                location: 'Field B',
                moistureLevel: 45,
                temperature: 26,
                humidity: 72,
                rainfall: 0,
                notes: 'Moisture below optimal, consider irrigation'
            }
        ];
    }

    async loadAlerts() {
        this.soilHealthData.alerts = [
            {
                id: 1,
                title: 'Low Soil Moisture Alert',
                message: 'Field B moisture level is below optimal (45%). Consider irrigation.',
                severity: 'Medium',
                location: 'Field B',
                isActive: true,
                createdAt: '2025-01-15T10:00:00Z'
            },
            {
                id: 2,
                title: 'pH Level Warning',
                message: 'Field B pH level is 5.2 (acidic). Consider lime application.',
                severity: 'High',
                location: 'Field B',
                isActive: true,
                createdAt: '2025-01-10T15:00:00Z'
            }
        ];
    }

    renderSoilHealthData() {
        this.renderSoilTests();
        this.renderSoilTypes();
        this.renderRecommendations();
        this.renderMonitoringData();
        this.renderAlerts();
    }

    renderSoilTests() {
        const container = document.getElementById('soil-tests');
        if (!container) return;

        if (this.soilHealthData.soilTests.length === 0) {
            container.innerHTML = '<div class="empty-state">No soil tests available</div>';
            return;
        }

        container.innerHTML = this.soilHealthData.soilTests.map(test => `
            <div class="soil-test-card" data-aos="fade-up">
                <div class="test-header">
                    <h3>Soil Test - ${test.location}</h3>
                    <span class="test-date">${this.formatDate(test.testDate)}</span>
                </div>
                <div class="test-results">
                    <div class="result-item">
                        <span class="label">pH Level:</span>
                        <span class="value ${this.getPHClass(test.phLevel)}">${test.phLevel}</span>
                    </div>
                    <div class="result-item">
                        <span class="label">Organic Matter:</span>
                        <span class="value">${test.organicMatter}%</span>
                    </div>
                    <div class="result-item">
                        <span class="label">Nitrogen (N):</span>
                        <span class="value">${test.nitrogen} kg/ha</span>
                    </div>
                    <div class="result-item">
                        <span class="label">Phosphorus (P):</span>
                        <span class="value">${test.phosphorus} kg/ha</span>
                    </div>
                    <div class="result-item">
                        <span class="label">Potassium (K):</span>
                        <span class="value">${test.potassium} kg/ha</span>
                    </div>
                </div>
                <div class="test-recommendations">
                    <strong>Recommendations:</strong> ${test.recommendations}
                </div>
                <button class="btn btn-primary" onclick="SoilHealth.viewTestDetails(${test.id})">
                    View Details
                </button>
            </div>
        `).join('');
    }

    renderSoilTypes() {
        const container = document.getElementById('soil-types');
        if (!container) return;

        container.innerHTML = this.soilHealthData.soilTypes.map(soilType => `
            <div class="soil-type-card" data-aos="fade-up">
                <div class="soil-image">
                    <img src="${soilType.image}" alt="${soilType.name}">
                </div>
                <div class="soil-content">
                    <h3>${soilType.name}</h3>
                    <p>${soilType.description}</p>
                    <div class="soil-characteristics">
                        <strong>Characteristics:</strong> ${soilType.characteristics}
                    </div>
                    <div class="suitable-crops">
                        <strong>Suitable Crops:</strong> ${soilType.suitableCrops.join(', ')}
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderRecommendations() {
        const container = document.getElementById('soil-recommendations');
        if (!container) return;

        container.innerHTML = this.soilHealthData.recommendations.map(rec => `
            <div class="recommendation-card" data-aos="fade-up">
                <div class="rec-header">
                    <h3>${rec.title}</h3>
                    <span class="rec-type">${rec.type}</span>
                </div>
                <p>${rec.description}</p>
                <div class="rec-details">
                    <div class="detail-item">
                        <span class="label">Application Rate:</span>
                        <span class="value">${rec.applicationRate}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Method:</span>
                        <span class="value">${rec.applicationMethod}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Timing:</span>
                        <span class="value">${rec.timing}</span>
                    </div>
                </div>
                <div class="rec-precautions">
                    <strong>Precautions:</strong> ${rec.precautions}
                </div>
            </div>
        `).join('');
    }

    renderMonitoringData() {
        const container = document.getElementById('soil-monitoring');
        if (!container) return;

        container.innerHTML = this.soilHealthData.monitoringData.map(data => `
            <div class="monitoring-card" data-aos="fade-up">
                <div class="monitoring-header">
                    <h3>${data.location}</h3>
                    <span class="monitoring-date">${this.formatDate(data.date)}</span>
                </div>
                <div class="monitoring-metrics">
                    <div class="metric">
                        <i class="fas fa-tint"></i>
                        <span class="metric-value">${data.moistureLevel}%</span>
                        <span class="metric-label">Moisture</span>
                    </div>
                    <div class="metric">
                        <i class="fas fa-thermometer-half"></i>
                        <span class="metric-value">${data.temperature}°C</span>
                        <span class="metric-label">Temperature</span>
                    </div>
                    <div class="metric">
                        <i class="fas fa-cloud"></i>
                        <span class="metric-value">${data.humidity}%</span>
                        <span class="metric-label">Humidity</span>
                    </div>
                </div>
                <div class="monitoring-notes">
                    <strong>Notes:</strong> ${data.notes}
                </div>
            </div>
        `).join('');
    }

    renderAlerts() {
        const container = document.getElementById('soil-alerts');
        if (!container) return;

        if (this.soilHealthData.alerts.length === 0) {
            container.innerHTML = '<div class="empty-state">No active alerts</div>';
            return;
        }

        container.innerHTML = this.soilHealthData.alerts.map(alert => `
            <div class="alert-card ${alert.severity.toLowerCase()}" data-aos="fade-up">
                <div class="alert-header">
                    <h4>${alert.title}</h4>
                    <span class="severity-badge ${alert.severity.toLowerCase()}">${alert.severity}</span>
                </div>
                <p>${alert.message}</p>
                <div class="alert-footer">
                    <span class="location"><i class="fas fa-map-marker-alt"></i> ${alert.location}</span>
                    <span class="alert-date">${this.formatDate(alert.createdAt)}</span>
                </div>
                <button class="btn btn-secondary" onclick="SoilHealth.dismissAlert(${alert.id})">
                    Dismiss
                </button>
            </div>
        `).join('');
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-schedule-test')) {
                this.showScheduleTestModal();
            }
            if (e.target.matches('.btn-add-monitoring')) {
                this.showAddMonitoringModal();
            }
        });
    }

    // Soil Health Actions
    viewTestDetails(testId) {
        const test = this.soilHealthData.soilTests.find(t => t.id === testId);
        if (test) {
            this.showNotification(`Viewing soil test details for ${test.location}`, 'info');
        }
    }

    dismissAlert(alertId) {
        const alert = this.soilHealthData.alerts.find(a => a.id === alertId);
        if (alert) {
            this.showNotification(`Alert dismissed: ${alert.title}`, 'success');
            // In a real app, this would update the alert status
        }
    }

    showScheduleTestModal() {
        if (!this.currentUser) {
            this.showNotification('Please login to schedule soil tests', 'warning');
            return;
        }

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Schedule Soil Test</h2>
                <form id="schedule-test-form" class="auth-form">
                    <div class="form-group">
                        <input type="text" id="test-location" placeholder="Field/Location Name" required>
                    </div>
                    <div class="form-group">
                        <select id="test-depth" required>
                            <option value="">Select Soil Depth</option>
                            <option value="0-15 cm">0-15 cm (Surface)</option>
                            <option value="15-30 cm">15-30 cm (Subsurface)</option>
                            <option value="30-60 cm">30-60 cm (Deep)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <input type="date" id="test-date" required>
                    </div>
                    <div class="form-group">
                        <textarea id="test-notes" placeholder="Additional Notes (Optional)" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary btn-full">Schedule Test</button>
                </form>
            </div>
        `;

        document.body.appendChild(modal);
        this.setupModalEventListeners(modal);
    }

    showAddMonitoringModal() {
        if (!this.currentUser) {
            this.showNotification('Please login to add monitoring data', 'warning');
            return;
        }

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Add Monitoring Data</h2>
                <form id="add-monitoring-form" class="auth-form">
                    <div class="form-group">
                        <input type="text" id="monitoring-location" placeholder="Field/Location" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <input type="number" id="moisture-level" placeholder="Moisture %" min="0" max="100" required>
                        </div>
                        <div class="form-group">
                            <input type="number" id="temperature" placeholder="Temperature °C" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <input type="number" id="humidity" placeholder="Humidity %" min="0" max="100" required>
                        </div>
                        <div class="form-group">
                            <input type="number" id="rainfall" placeholder="Rainfall (mm)" min="0" step="0.1">
                        </div>
                    </div>
                    <div class="form-group">
                        <textarea id="monitoring-notes" placeholder="Notes (Optional)" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary btn-full">Add Data</button>
                </form>
            </div>
        `;

        document.body.appendChild(modal);
        this.setupModalEventListeners(modal);
    }

    setupModalEventListeners(modal) {
        const closeBtn = modal.querySelector('.close');
        const form = modal.querySelector('form');

        closeBtn.onclick = () => modal.remove();
        
        modal.onclick = (e) => {
            if (e.target === modal) modal.remove();
        };

        if (form) {
            form.onsubmit = (e) => {
                e.preventDefault();
                this.handleFormSubmission(form, modal);
            };
        }
    }

    handleFormSubmission(form, modal) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Simulate API call
        setTimeout(() => {
            this.showNotification('Data submitted successfully!', 'success');
            modal.remove();
            // In a real app, this would refresh the data
        }, 1000);
    }

    // Utility Functions
    getPHClass(phLevel) {
        if (phLevel < 6.0) return 'acidic';
        if (phLevel > 7.5) return 'alkaline';
        return 'neutral';
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN');
    }

    showNotification(message, type = 'info') {
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }

    showSoilHealthError(message) {
        this.showNotification(message, 'error');
    }

    // Public API
    static getInstance() {
        if (!window.SoilHealth) {
            window.SoilHealth = new SoilHealthManager();
        }
        return window.SoilHealth;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    SoilHealthManager.getInstance().init();
});

window.SoilHealth = SoilHealthManager.getInstance();

