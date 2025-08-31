/**
 * FARMazee - Crops JavaScript
 * Handles crop management and monitoring
 */

// Crops state
let cropsData = {
    crops: [],
    activities: [],
    diseases: [],
    pests: []
};

// Initialize crops functionality
document.addEventListener('DOMContentLoaded', function() {
    initCrops();
});

/**
 * Initialize crops functionality
 */
function initCrops() {
    loadCropsData();
    setupCropUpdates();
}

/**
 * Load crops data
 */
async function loadCropsData() {
    try {
        const [crops, activities, diseases, pests] = await Promise.all([
            loadCropsList(),
            loadCropActivities(),
            loadCropDiseases(),
            loadCropPests()
        ]);
        
        cropsData.crops = crops;
        cropsData.activities = activities;
        cropsData.diseases = diseases;
        cropsData.pests = pests;
        
        renderCropsData();
        
    } catch (error) {
        console.error('Error loading crops data:', error);
        showCropsError('Failed to load crops data');
    }
}

/**
 * Load crops list
 */
async function loadCropsList() {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
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
            progress: 65,
            location: 'Field A',
            soilType: 'Loamy',
            irrigationType: 'Drip'
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
            progress: 95,
            location: 'Field B',
            soilType: 'Clay',
            irrigationType: 'Sprinkler'
        }
    ];
}

/**
 * Load crop activities
 */
async function loadCropActivities() {
    await new Promise(resolve => setTimeout(resolve, 800));
    
    return [
        {
            id: 1,
            cropId: 1,
            type: 'fertilization',
            date: '2025-01-25',
            description: 'Applied NPK fertilizer',
            status: 'completed'
        },
        {
            id: 2,
            cropId: 1,
            type: 'irrigation',
            date: '2025-01-28',
            description: 'Scheduled irrigation',
            status: 'pending'
        }
    ];
}

/**
 * Load crop diseases
 */
async function loadCropDiseases() {
    await new Promise(resolve => setTimeout(resolve, 600));
    
    return [
        {
            id: 1,
            cropId: 1,
            name: 'Rust',
            severity: 'low',
            detectedDate: '2025-01-20',
            treatment: 'Fungicide application recommended'
        }
    ];
}

/**
 * Load crop pests
 */
async function loadCropPests() {
    await new Promise(resolve => setTimeout(resolve, 400));
    
    return [
        {
            id: 1,
            cropId: 2,
            name: 'Corn Borer',
            severity: 'medium',
            detectedDate: '2025-01-22',
            treatment: 'Insecticide treatment required'
        }
    ];
}

/**
 * Render crops data
 */
function renderCropsData() {
    renderCropsOverview();
    renderCropsList();
    renderCropActivities();
    renderCropHealth();
}

/**
 * Render crops overview
 */
function renderCropsOverview() {
    const container = document.querySelector('.crops-overview');
    if (!container) return;
    
    const totalCrops = cropsData.crops.length;
    const totalArea = cropsData.crops.reduce((sum, crop) => sum + crop.area, 0);
    const healthyCrops = cropsData.crops.filter(crop => crop.health > 80).length;
    const readyToHarvest = cropsData.crops.filter(crop => crop.status === 'harvest-ready').length;
    
    container.innerHTML = `
        <h3>Crops Overview</h3>
        <div class="crops-stats">
            <div class="stat-box">
                <span class="number">${totalCrops}</span>
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
            <div class="stat-box">
                <span class="number">${readyToHarvest}</span>
                <span class="label">Ready to Harvest</span>
            </div>
        </div>
    `;
}

/**
 * Render crops list
 */
function renderCropsList() {
    const container = document.querySelector('.crops-list');
    if (!container) return;
    
    container.innerHTML = `
        <h3>Your Crops</h3>
        <div class="crops-grid">
            ${cropsData.crops.map(crop => `
                <div class="crop-card ${crop.status}">
                    <div class="crop-header">
                        <h4>${crop.name} - ${crop.variety}</h4>
                        <span class="crop-status ${crop.status}">${crop.status}</span>
                    </div>
                    <div class="crop-image">
                        <i class="fas fa-seedling"></i>
                    </div>
                    <div class="crop-content">
                        <div class="crop-info">
                            <p><strong>Location:</strong> ${crop.location}</p>
                            <p><strong>Area:</strong> ${crop.area} ha</p>
                            <p><strong>Health:</strong> ${crop.health}%</p>
                        </div>
                        <div class="crop-progress">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${crop.progress}%"></div>
                            </div>
                            <span>${crop.progress}% Complete</span>
                        </div>
                        <div class="crop-actions">
                            <button class="btn btn-sm btn-primary" onclick="viewCropDetails(${crop.id})">
                                <i class="fas fa-eye"></i> View
                            </button>
                            <button class="btn btn-sm btn-secondary" onclick="editCrop(${crop.id})">
                                <i class="fas fa-edit"></i> Edit
                            </button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
        <div class="add-crop-section">
            <button class="btn btn-primary" onclick="showAddCropModal()">
                <i class="fas fa-plus"></i> Add New Crop
            </button>
        </div>
    `;
}

/**
 * Render crop activities
 */
function renderCropActivities() {
    const container = document.querySelector('.crop-activities');
    if (!container) return;
    
    container.innerHTML = `
        <h3>Recent Activities</h3>
        <div class="activities-list">
            ${cropsData.activities.map(activity => `
                <div class="activity-item ${activity.status}">
                    <div class="activity-icon">
                        <i class="fas fa-${getActivityIcon(activity.type)}"></i>
                    </div>
                    <div class="activity-content">
                        <h4>${activity.description}</h4>
                        <p>${formatDate(activity.date)}</p>
                    </div>
                    <div class="activity-status">
                        <span class="status-badge ${activity.status}">${activity.status}</span>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render crop health
 */
function renderCropHealth() {
    const container = document.querySelector('.crop-health');
    if (!container) return;
    
    const healthIssues = [...cropsData.diseases, ...cropsData.pests];
    
    if (healthIssues.length === 0) {
        container.innerHTML = `
            <h3>Crop Health</h3>
            <p class="no-issues">All crops are healthy! No issues detected.</p>
        `;
        return;
    }
    
    container.innerHTML = `
        <h3>Crop Health Issues</h3>
        <div class="health-issues">
            ${healthIssues.map(issue => `
                <div class="health-issue ${issue.severity}">
                    <div class="issue-header">
                        <h4>${issue.name}</h4>
                        <span class="severity-badge ${issue.severity}">${issue.severity}</span>
                    </div>
                    <p><strong>Crop:</strong> ${getCropName(issue.cropId)}</p>
                    <p><strong>Detected:</strong> ${formatDate(issue.detectedDate)}</p>
                    <p><strong>Treatment:</strong> ${issue.treatment}</p>
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Show add crop modal
 */
function showAddCropModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>Add New Crop</h2>
            <form id="add-crop-form" class="crop-form">
                <div class="form-group">
                    <label for="crop-name">Crop Name</label>
                    <input type="text" id="crop-name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="crop-variety">Variety</label>
                    <input type="text" id="crop-variety" name="variety" required>
                </div>
                <div class="form-group">
                    <label for="crop-area">Area (hectares)</label>
                    <input type="number" id="crop-area" name="area" step="0.1" required>
                </div>
                <div class="form-group">
                    <label for="crop-location">Location</label>
                    <input type="text" id="crop-location" name="location" required>
                </div>
                <div class="form-group">
                    <label for="planted-date">Planted Date</label>
                    <input type="date" id="planted-date" name="plantedDate" required>
                </div>
                <button type="submit" class="btn btn-primary">Add Crop</button>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal functionality
    const closeBtn = modal.querySelector('.close');
    closeBtn.onclick = () => modal.remove();
    
    // Form submission
    const form = modal.querySelector('#add-crop-form');
    form.onsubmit = handleAddCrop;
}

/**
 * Handle add crop form submission
 */
async function handleAddCrop(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const cropData = {
        name: formData.get('name'),
        variety: formData.get('variety'),
        area: parseFloat(formData.get('area')),
        location: formData.get('location'),
        plantedDate: formData.get('plantedDate')
    };
    
    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Add to local state
        const newCrop = {
            id: Date.now(),
            ...cropData,
            status: 'growing',
            health: 100,
            progress: 0,
            soilType: 'Unknown',
            irrigationType: 'Unknown'
        };
        
        cropsData.crops.push(newCrop);
        renderCropsData();
        
        // Close modal
        e.target.closest('.modal').remove();
        
        // Show success message
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification('Crop added successfully!', 'success');
        }
        
    } catch (error) {
        console.error('Error adding crop:', error);
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification('Failed to add crop. Please try again.', 'error');
        }
    }
}

/**
 * View crop details
 */
function viewCropDetails(cropId) {
    const crop = cropsData.crops.find(c => c.id === cropId);
    if (!crop) return;
    
    // Show crop details modal
    showCropDetailsModal(crop);
}

/**
 * Edit crop
 */
function editCrop(cropId) {
    const crop = cropsData.crops.find(c => c.id === cropId);
    if (!crop) return;
    
    // Show edit crop modal
    showEditCropModal(crop);
}

/**
 * Setup crop updates
 */
function setupCropUpdates() {
    // Update crop progress every hour
    setInterval(updateCropProgress, 60 * 60 * 1000);
    
    // Check for health issues every 6 hours
    setInterval(checkCropHealth, 6 * 60 * 60 * 1000);
}

/**
 * Update crop progress
 */
function updateCropProgress() {
    cropsData.crops.forEach(crop => {
        if (crop.status === 'growing' && crop.progress < 100) {
            crop.progress += Math.random() * 5; // Random progress increase
            if (crop.progress >= 100) {
                crop.status = 'harvest-ready';
                crop.progress = 100;
            }
        }
    });
    
    renderCropsData();
}

/**
 * Check crop health
 */
function checkCropHealth() {
    // Simulate health monitoring
    cropsData.crops.forEach(crop => {
        if (crop.health > 50) {
            crop.health -= Math.random() * 5; // Random health decrease
        }
    });
    
    renderCropsData();
}

/**
 * Show crops error
 */
function showCropsError(message) {
    const container = document.querySelector('.crops-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="error-state">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Failed to Load Crops</h3>
            <p>${message}</p>
            <button class="btn btn-primary" onclick="loadCropsData()">
                <i class="fas fa-refresh"></i>
                Try Again
            </button>
        </div>
    `;
}

/**
 * Utility functions
 */
function getActivityIcon(type) {
    const icons = {
        fertilization: 'leaf',
        irrigation: 'tint',
        harvesting: 'cut',
        planting: 'seedling',
        spraying: 'spray-can',
        default: 'cog'
    };
    return icons[type] || icons.default;
}

function getCropName(cropId) {
    const crop = cropsData.crops.find(c => c.id === cropId);
    return crop ? crop.name : 'Unknown';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Export functions for use in other modules
window.Crops = {
    initCrops,
    loadCropsData,
    renderCropsData,
    showAddCropModal,
    viewCropDetails,
    editCrop
};

