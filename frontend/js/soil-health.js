// Soil Health Management for Farmazee
// Handles soil health monitoring, testing, recommendations, and analysis

class SoilHealthManager {
    constructor() {
        this.soilData = {
            tests: [],
            recommendations: [],
            monitoringData: [],
            soilTypes: [],
            nutrients: []
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
                this.loadRecommendations(),
                this.loadMonitoringData(),
                this.loadSoilTypes(),
                this.loadNutrients()
            ]);
            
            this.renderSoilHealthData();
        } catch (error) {
            console.error('Error loading soil health data:', error);
            this.showSoilHealthError('Failed to load soil health data');
        }
    }

    async loadSoilTests() {
        // Simulate API call
        this.soilData.tests = [
            {
                id: 1,
                testType: 'Comprehensive',
                testDate: '2025-01-10T09:00:00Z',
                location: 'Field A - North Section',
                depth: '0-30 cm',
                status: 'Completed',
                results: {
                    pH: 6.8,
                    organicMatter: 2.1,
                    nitrogen: 45,
                    phosphorus: 28,
                    potassium: 180,
                    calcium: 320,
                    magnesium: 85
                },
                recommendations: 'Soil is slightly acidic, good organic matter content. Consider adding phosphorus for better crop growth.'
            },
            {
                id: 2,
                testType: 'Basic',
                testDate: '2024-12-15T14:30:00Z',
                location: 'Field B - South Section',
                depth: '0-15 cm',
                status: 'Completed',
                results: {
                    pH: 7.2,
                    organicMatter: 1.8,
                    nitrogen: 38,
                    phosphorus: 35,
                    potassium: 165
                },
                recommendations: 'Soil pH is optimal. Consider adding organic matter and nitrogen for improved fertility.'
            }
        ];
    }

    async loadRecommendations() {
        // Simulate API call
        this.soilData.recommendations = [
            {
                id: 1,
                crop: 'Rice',
                soilType: 'Clay Loam',
                season: 'Kharif',
                recommendations: [
                    'Apply 120 kg N, 60 kg P2O5, and 40 kg K2O per hectare',
                    'Maintain 5-7 cm water level during initial growth',
                    'Use organic matter to improve soil structure',
                    'Monitor pH levels (optimal: 6.0-7.0)'
                ],
                fertilizers: [
                    { name: 'Urea', amount: '130 kg/ha', timing: 'Split application' },
                    { name: 'DAP', amount: '130 kg/ha', timing: 'Basal' },
                    { name: 'MOP', amount: '65 kg/ha', timing: 'Basal' }
                ]
            },
            {
                id: 2,
                crop: 'Cotton',
                soilType: 'Black Soil',
                season: 'Kharif',
                recommendations: [
                    'Apply 150 kg N, 75 kg P2O5, and 50 kg K2O per hectare',
                    'Ensure proper drainage for black soil',
                    'Use micronutrients if deficiency observed',
                    'Maintain soil moisture during flowering'
                ],
                fertilizers: [
                    { name: 'Urea', amount: '160 kg/ha', timing: 'Split application' },
                    { name: 'DAP', amount: '160 kg/ha', timing: 'Basal' },
                    { name: 'MOP', amount: '80 kg/ha', timing: 'Basal' }
                ]
            }
        ];
    }

    async loadMonitoringData() {
        // Simulate API call
        this.soilData.monitoringData = [
            {
                id: 1,
                date: '2025-01-15T08:00:00Z',
                location: 'Field A',
                moisture: 65,
                temperature: 28,
                humidity: 75,
                rainfall: 0,
                notes: 'Soil moisture optimal for current crop stage'
            },
            {
                id: 2,
                date: '2025-01-14T08:00:00Z',
                location: 'Field A',
                moisture: 58,
                temperature: 30,
                humidity: 70,
                rainfall: 0,
                notes: 'Moisture decreasing, consider irrigation'
            }
        ];
    }

    async loadSoilTypes() {
        // Simulate API call
        this.soilData.soilTypes = [
            {
                id: 1,
                name: 'Clay Loam',
                description: 'Good water retention, suitable for rice and vegetables',
                characteristics: ['High water retention', 'Good nutrient holding', 'Slow drainage'],
                suitableCrops: ['Rice', 'Vegetables', 'Fruits'],
                image: './assets/images/soil-clay-loam.jpg'
            },
            {
                id: 2,
                name: 'Sandy Loam',
                description: 'Well-draining soil, good for root crops and pulses',
                characteristics: ['Good drainage', 'Easy to work', 'Warms quickly'],
                suitableCrops: ['Groundnut', 'Pulses', 'Root vegetables'],
                image: './assets/images/soil-sandy-loam.jpg'
            },
            {
                id: 3,
                name: 'Red Soil',
                description: 'Rich in iron, suitable for cotton and millets',
                characteristics: ['Rich in iron', 'Good for cotton', 'Requires organic matter'],
                suitableCrops: ['Cotton', 'Millets', 'Pulses'],
                image: './assets/images/soil-red-soil.jpg'
            },
            {
                id: 4,
                name: 'Black Soil',
                description: 'High clay content, excellent for cotton and sugarcane',
                characteristics: ['High clay content', 'Good water retention', 'Rich in minerals'],
                suitableCrops: ['Cotton', 'Sugarcane', 'Wheat'],
                image: './assets/images/soil-black-soil.jpg'
            }
        ];
    }

    async loadNutrients() {
        // Simulate API call
        this.soilData.nutrients = [
            {
                id: 1,
                name: 'Nitrogen (N)',
                symbol: 'N',
                function: 'Essential for leaf growth and chlorophyll production',
                deficiencySymptoms: ['Yellow leaves', 'Stunted growth', 'Poor yield'],
                sources: ['Urea', 'Ammonium sulfate', 'Organic matter'],
                optimalRange: '40-60 kg/ha'
            },
            {
                id: 2,
                name: 'Phosphorus (P)',
                symbol: 'P',
                function: 'Important for root development and flowering',
                deficiencySymptoms: ['Purple leaves', 'Poor root growth', 'Delayed maturity'],
                sources: ['DAP', 'SSP', 'Bone meal'],
                optimalRange: '25-40 kg/ha'
            },
            {
                id: 3,
                name: 'Potassium (K)',
                symbol: 'K',
                function: 'Helps in disease resistance and fruit quality',
                deficiencySymptoms: ['Brown leaf edges', 'Weak stems', 'Poor fruit quality'],
                sources: ['MOP', 'SOP', 'Wood ash'],
                optimalRange: '30-50 kg/ha'
            }
        ];
    }

    renderSoilHealthData() {
        this.renderSoilTests();
        this.renderRecommendations();
        this.renderMonitoringData();
        this.renderSoilTypes();
        this.renderNutrients();
    }

    renderSoilTests() {
        const testsContainer = document.getElementById('soil-tests');
        if (!testsContainer) return;

        if (this.soilData.tests.length === 0) {
            testsContainer.innerHTML = '<p>No soil tests available</p>';
            return;
        }

        const testsHTML = this.soilData.tests.map(test => `
            <div class="soil-test-card" data-aos="fade-up">
                <div class="test-header">
                    <h3>${test.testType} Soil Test</h3>
                    <span class="status-badge ${test.status.toLowerCase()}">${test.status}</span>
                </div>
                
                <div class="test-details">
                    <div class="detail-item">
                        <strong>Date:</strong> ${this.formatDate(test.testDate)}
                    </div>
                    <div class="detail-item">
                        <strong>Location:</strong> ${test.location}
                    </div>
                    <div class="detail-item">
                        <strong>Depth:</strong> ${test.depth}
                    </div>
                </div>

                <div class="test-results">
                    <h4>Test Results:</h4>
                    <div class="results-grid">
                        ${Object.entries(test.results).map(([parameter, value]) => `
                            <div class="result-item">
                                <span class="parameter">${parameter.toUpperCase()}</span>
                                <span class="value">${value}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="test-recommendations">
                    <h4>Recommendations:</h4>
                    <p>${test.recommendations}</p>
                </div>

                <div class="test-actions">
                    <button class="btn btn-secondary" onclick="SoilHealth.viewTestDetails(${test.id})">
                        View Details
                    </button>
                    <button class="btn btn-primary" onclick="SoilHealth.downloadReport(${test.id})">
                        Download Report
                    </button>
                </div>
            </div>
        `).join('');

        testsContainer.innerHTML = testsHTML;
    }

    renderRecommendations() {
        const recommendationsContainer = document.getElementById('soil-recommendations');
        if (!recommendationsContainer) return;

        if (this.soilData.recommendations.length === 0) {
            recommendationsContainer.innerHTML = '<p>No recommendations available</p>';
            return;
        }

        const recommendationsHTML = this.soilData.recommendations.map(rec => `
            <div class="recommendation-card" data-aos="fade-up">
                <div class="rec-header">
                    <h3>${rec.crop} - ${rec.soilType}</h3>
                    <span class="season-badge">${rec.season}</span>
                </div>

                <div class="rec-content">
                    <div class="rec-section">
                        <h4>General Recommendations:</h4>
                        <ul>
                            ${rec.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>

                    <div class="rec-section">
                        <h4>Fertilizer Schedule:</h4>
                        <div class="fertilizer-list">
                            ${rec.fertilizers.map(fert => `
                                <div class="fertilizer-item">
                                    <span class="name">${fert.name}</span>
                                    <span class="amount">${fert.amount}</span>
                                    <span class="timing">${fert.timing}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <div class="rec-actions">
                    <button class="btn btn-primary" onclick="SoilHealth.applyRecommendations(${rec.id})">
                        Apply Recommendations
                    </button>
                    <button class="btn btn-secondary" onclick="SoilHealth.saveRecommendations(${rec.id})">
                        Save for Later
                    </button>
                </div>
            </div>
        `).join('');

        recommendationsContainer.innerHTML = recommendationsHTML;
    }

    renderMonitoringData() {
        const monitoringContainer = document.getElementById('soil-monitoring');
        if (!monitoringContainer) return;

        if (this.soilData.monitoringData.length === 0) {
            monitoringContainer.innerHTML = '<p>No monitoring data available</p>';
            return;
        }

        const monitoringHTML = this.soilData.monitoringData.map(data => `
            <div class="monitoring-card" data-aos="fade-up">
                <div class="monitoring-header">
                    <h3>${data.location}</h3>
                    <span class="date">${this.formatDate(data.date)}</span>
                </div>

                <div class="monitoring-metrics">
                    <div class="metric">
                        <i class="fas fa-tint"></i>
                        <span class="label">Moisture</span>
                        <span class="value">${data.moisture}%</span>
                    </div>
                    <div class="metric">
                        <i class="fas fa-thermometer-half"></i>
                        <span class="label">Temperature</span>
                        <span class="value">${data.temperature}°C</span>
                    </div>
                    <div class="metric">
                        <i class="fas fa-cloud"></i>
                        <span class="label">Humidity</span>
                        <span class="value">${data.humidity}%</span>
                    </div>
                    <div class="metric">
                        <i class="fas fa-cloud-rain"></i>
                        <span class="label">Rainfall</span>
                        <span class="value">${data.rainfall} mm</span>
                    </div>
                </div>

                <div class="monitoring-notes">
                    <strong>Notes:</strong> ${data.notes}
                </div>

                <div class="monitoring-actions">
                    <button class="btn btn-secondary" onclick="SoilHealth.viewMonitoringDetails(${data.id})">
                        View Details
                    </button>
                </div>
            </div>
        `).join('');

        monitoringContainer.innerHTML = monitoringHTML;
    }

    renderSoilTypes() {
        const soilTypesContainer = document.getElementById('soil-types');
        if (!soilTypesContainer) return;

        const soilTypesHTML = this.soilData.soilTypes.map(soilType => `
            <div class="soil-type-card" data-aos="fade-up">
                <div class="soil-type-image">
                    <div class="image-placeholder">
                        <i class="fas fa-seedling"></i>
                    </div>
                </div>
                <div class="soil-type-content">
                    <h3>${soilType.name}</h3>
                    <p>${soilType.description}</p>
                    
                    <div class="soil-characteristics">
                        <h4>Characteristics:</h4>
                        <ul>
                            ${soilType.characteristics.map(char => `<li>${char}</li>`).join('')}
                        </ul>
                    </div>

                    <div class="suitable-crops">
                        <h4>Suitable Crops:</h4>
                        <div class="crop-tags">
                            ${soilType.suitableCrops.map(crop => `<span class="crop-tag">${crop}</span>`).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        soilTypesContainer.innerHTML = soilTypesHTML;
    }

    renderNutrients() {
        const nutrientsContainer = document.getElementById('soil-nutrients');
        if (!nutrientsContainer) return;

        const nutrientsHTML = this.soilData.nutrients.map(nutrient => `
            <div class="nutrient-card" data-aos="fade-up">
                <div class="nutrient-header">
                    <h3>${nutrient.name} (${nutrient.symbol})</h3>
                </div>
                
                <div class="nutrient-content">
                    <p><strong>Function:</strong> ${nutrient.function}</p>
                    
                    <div class="nutrient-details">
                        <div class="detail-section">
                            <h4>Deficiency Symptoms:</h4>
                            <ul>
                                ${nutrient.deficiencySymptoms.map(symptom => `<li>${symptom}</li>`).join('')}
                            </ul>
                        </div>

                        <div class="detail-section">
                            <h4>Sources:</h4>
                            <ul>
                                ${nutrient.sources.map(source => `<li>${source}</li>`).join('')}
                            </ul>
                        </div>

                        <div class="detail-section">
                            <h4>Optimal Range:</h4>
                            <p>${nutrient.optimalRange}</p>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        nutrientsContainer.innerHTML = nutrientsHTML;
    }

    setupEventListeners() {
        // Add event listeners for soil health interactions
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
        const test = this.soilData.tests.find(t => t.id === testId);
        if (test) {
            this.showNotification(`Viewing test details for ${test.testType}`, 'info');
            // In a real app, this would show detailed test results
        }
    }

    downloadReport(testId) {
        const test = this.soilData.tests.find(t => t.id === testId);
        if (test) {
            this.showNotification(`Downloading report for ${test.testType}`, 'success');
            // In a real app, this would generate and download a PDF report
        }
    }

    applyRecommendations(recId) {
        const rec = this.soilData.recommendations.find(r => r.id === recId);
        if (rec) {
            this.showNotification(`Applying recommendations for ${rec.crop}`, 'success');
            // In a real app, this would create a task or reminder
        }
    }

    saveRecommendations(recId) {
        const rec = this.soilData.recommendations.find(r => r.id === recId);
        if (rec) {
            this.showNotification(`Saved recommendations for ${rec.crop}`, 'success');
            // In a real app, this would save to user's saved items
        }
    }

    viewMonitoringDetails(dataId) {
        const data = this.soilData.monitoringData.find(d => d.id === dataId);
        if (data) {
            this.showNotification(`Viewing monitoring data for ${data.location}`, 'info');
            // In a real app, this would show detailed monitoring data
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
                        <label>Test Type</label>
                        <select id="test-type" required>
                            <option value="">Select test type</option>
                            <option value="Basic">Basic Test</option>
                            <option value="Comprehensive">Comprehensive Test</option>
                            <option value="Specialized">Specialized Test</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Field Location</label>
                        <input type="text" id="field-location" placeholder="Enter field location" required>
                    </div>
                    <div class="form-group">
                        <label>Test Depth</label>
                        <select id="test-depth" required>
                            <option value="">Select depth</option>
                            <option value="0-15 cm">0-15 cm</option>
                            <option value="15-30 cm">15-30 cm</option>
                            <option value="30-60 cm">30-60 cm</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Preferred Date</label>
                        <input type="date" id="preferred-date" required>
                    </div>
                    <div class="form-group">
                        <label>Additional Notes</label>
                        <textarea id="notes" placeholder="Any specific requirements or concerns..." rows="3"></textarea>
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
                        <label>Field Location</label>
                        <input type="text" id="monitoring-location" placeholder="Enter field location" required>
                    </div>
                    <div class="form-group">
                        <label>Soil Moisture (%)</label>
                        <input type="number" id="moisture" min="0" max="100" placeholder="Enter moisture percentage" required>
                    </div>
                    <div class="form-group">
                        <label>Soil Temperature (°C)</label>
                        <input type="number" id="temperature" min="0" max="50" placeholder="Enter temperature" required>
                    </div>
                    <div class="form-group">
                        <label>Humidity (%)</label>
                        <input type="number" id="humidity" min="0" max="100" placeholder="Enter humidity percentage" required>
                    </div>
                    <div class="form-group">
                        <label>Rainfall (mm)</label>
                        <input type="number" id="rainfall" min="0" placeholder="Enter rainfall amount" required>
                    </div>
                    <div class="form-group">
                        <label>Notes</label>
                        <textarea id="monitoring-notes" placeholder="Any observations or notes..." rows="3"></textarea>
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
            this.showNotification('Submitted successfully!', 'success');
            modal.remove();
            // In a real app, this would refresh the soil health data
        }, 1000);
    }

    // Utility Functions
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
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
}

// Initialize Soil Health Manager
document.addEventListener('DOMContentLoaded', () => {
    SoilHealthManager.getInstance().init();
});

// Export for global access
window.SoilHealth = SoilHealthManager.getInstance();

