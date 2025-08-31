// Government Schemes Management for Farmazee
// Handles government schemes, subsidies, applications, and eligibility checking

class SchemesManager {
    constructor() {
        this.schemesData = {
            schemes: [],
            categories: [],
            userApplications: []
        };
        this.currentUser = null;
        this.isInitialized = false;
    }

    init() {
        if (this.isInitialized) return;
        
        this.currentUser = this.getCurrentUser();
        this.loadSchemesData();
        this.setupEventListeners();
        this.isInitialized = true;
        
        console.log('Schemes Manager initialized');
    }

    getCurrentUser() {
        const userStr = localStorage.getItem('farmazee_user');
        return userStr ? JSON.parse(userStr) : null;
    }

    async loadSchemesData() {
        try {
            await Promise.all([
                this.loadSchemes(),
                this.loadCategories(),
                this.loadUserApplications()
            ]);
            
            this.renderSchemesData();
        } catch (error) {
            console.error('Error loading schemes data:', error);
            this.showSchemesError('Failed to load schemes data');
        }
    }

    async loadSchemes() {
        // Simulate API call
        this.schemesData.schemes = [
            {
                id: 1,
                name: 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
                description: 'Direct income support of ₹6,000 per year to eligible farmer families',
                category: 'Income Support',
                status: 'Active',
                maxBenefit: '₹6,000 per year',
                applicationFee: 0,
                isOpen: true
            },
            {
                id: 2,
                name: 'PM Fasal Bima Yojana (PMFBY)',
                description: 'Comprehensive crop insurance scheme for farmers against natural calamities',
                category: 'Crop Insurance',
                status: 'Active',
                maxBenefit: 'Up to 100% of sum insured',
                applicationFee: 'Varies by crop',
                isOpen: true
            },
            {
                id: 3,
                name: 'Soil Health Card Scheme',
                description: 'Free soil testing and recommendations for farmers',
                category: 'Soil Health',
                status: 'Active',
                maxBenefit: 'Free soil testing',
                applicationFee: 0,
                isOpen: true
            }
        ];
    }

    async loadCategories() {
        this.schemesData.categories = [
            { id: 1, name: 'Income Support', schemeCount: 1 },
            { id: 2, name: 'Crop Insurance', schemeCount: 1 },
            { id: 3, name: 'Soil Health', schemeCount: 1 }
        ];
    }

    async loadUserApplications() {
        if (!this.currentUser) return;
        
        this.schemesData.userApplications = [
            {
                id: 1,
                schemeName: 'PM-KISAN',
                status: 'Approved',
                amount: 6000
            }
        ];
    }

    renderSchemesData() {
        this.renderSchemes();
        this.renderCategories();
        this.renderUserApplications();
    }

    renderSchemes() {
        const schemesContainer = document.getElementById('schemes-list');
        if (!schemesContainer) return;

        const schemesHTML = this.schemesData.schemes.map(scheme => `
            <div class="scheme-card" data-aos="fade-up">
                <div class="scheme-header">
                    <h3>${scheme.name}</h3>
                    <span class="status-badge ${scheme.status.toLowerCase()}">${scheme.status}</span>
                </div>
                <p class="scheme-description">${scheme.description}</p>
                <div class="scheme-details">
                    <span><strong>Category:</strong> ${scheme.category}</span>
                    <span><strong>Max Benefit:</strong> ${scheme.maxBenefit}</span>
                </div>
                <div class="scheme-actions">
                    <button class="btn btn-primary" onclick="Schemes.applyForScheme(${scheme.id})">
                        Apply Now
                    </button>
                </div>
            </div>
        `).join('');

        schemesContainer.innerHTML = schemesHTML;
    }

    renderCategories() {
        const categoriesContainer = document.getElementById('schemes-categories');
        if (!categoriesContainer) return;

        const categoriesHTML = this.schemesData.categories.map(category => `
            <div class="category-card" data-aos="fade-up">
                <h3>${category.name}</h3>
                <p>${category.schemeCount} schemes available</p>
            </div>
        `).join('');

        categoriesContainer.innerHTML = categoriesHTML;
    }

    renderUserApplications() {
        const applicationsContainer = document.getElementById('user-applications');
        if (!applicationsContainer) return;

        if (!this.currentUser) {
            applicationsContainer.innerHTML = '<p>Please login to view applications</p>';
            return;
        }

        if (this.schemesData.userApplications.length === 0) {
            applicationsContainer.innerHTML = '<p>No applications yet</p>';
            return;
        }

        const applicationsHTML = this.schemesData.userApplications.map(app => `
            <div class="application-card">
                <h4>${app.schemeName}</h4>
                <p>Status: ${app.status}</p>
                <p>Amount: ₹${app.amount}</p>
            </div>
        `).join('');

        applicationsContainer.innerHTML = applicationsHTML;
    }

    setupEventListeners() {
        // Add event listeners for schemes interactions
    }

    applyForScheme(schemeId) {
        if (!this.currentUser) {
            this.showNotification('Please login to apply for schemes', 'warning');
            return;
        }

        const scheme = this.schemesData.schemes.find(s => s.id === schemeId);
        if (scheme) {
            this.showNotification(`Applying for: ${scheme.name}`, 'success');
        }
    }

    showNotification(message, type = 'info') {
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }

    showSchemesError(message) {
        this.showNotification(message, 'error');
    }
}

// Initialize Schemes Manager
document.addEventListener('DOMContentLoaded', () => {
    SchemesManager.getInstance().init();
});

// Export for global access
window.Schemes = SchemesManager.getInstance();
