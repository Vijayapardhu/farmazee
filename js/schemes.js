// Government Schemes Management for Farmazee
class SchemesManager {
    constructor() {
        this.schemesData = {
            schemes: [],
            categories: [],
            applications: [],
            updates: []
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
                this.loadApplications(),
                this.loadUpdates()
            ]);
            this.renderSchemesData();
        } catch (error) {
            console.error('Error loading schemes data:', error);
            this.showSchemesError('Failed to load schemes data');
        }
    }

    async loadSchemes() {
        try {
            const response = await fetch('/api/schemes/');
            if (!response.ok) {
                throw new Error('Schemes API not available');
            }
            const data = await response.json();
            this.schemesData.schemes = data.results || [];
        } catch (error) {
            console.error('Error loading schemes:', error);
            // Fallback to mock data
            this.schemesData.schemes = [
                {
                    id: 1,
                    title: 'PM-KISAN Samman Nidhi',
                    description: 'Direct income support of ₹6,000 per year to eligible farmer families',
                    category: 'Income Support',
                    benefits: '₹6,000 per year in three equal installments',
                deadline: '2025-03-31T23:59:59Z',
                status: 'Active',
                isFeatured: true
            },
            {
                id: 2,
                title: 'PM Fasal Bima Yojana',
                description: 'Comprehensive crop insurance scheme for farmers',
                category: 'Crop Insurance',
                benefits: 'Up to 100% premium subsidy, comprehensive coverage',
                deadline: '2025-02-28T23:59:59Z',
                status: 'Active',
                isFeatured: true
            }
        ];
    }

    async loadCategories() {
        this.schemesData.categories = [
            { id: 1, name: 'Income Support', icon: 'fas fa-money-bill-wave' },
            { id: 2, name: 'Crop Insurance', icon: 'fas fa-shield-alt' },
            { id: 3, name: 'Soil Health', icon: 'fas fa-flask' }
        ];
    }

    async loadApplications() {
        if (!this.currentUser) return;
        this.schemesData.applications = [
            {
                id: 1,
                schemeTitle: 'PM-KISAN Samman Nidhi',
                status: 'Approved',
                appliedDate: '2025-01-10T10:00:00Z'
            }
        ];
    }

    async loadUpdates() {
        this.schemesData.updates = [
            {
                id: 1,
                title: 'PM-KISAN Installment Release',
                content: 'Second installment of ₹2,000 for FY 2024-25 has been released',
                date: '2025-01-15T10:00:00Z'
            }
        ];
    }

    renderSchemesData() {
        this.renderFeaturedSchemes();
        this.renderSchemeCategories();
        this.renderUserApplications();
        this.renderRecentUpdates();
    }

    renderFeaturedSchemes() {
        const container = document.getElementById('featured-schemes');
        if (!container) return;

        const featuredSchemes = this.schemesData.schemes.filter(s => s.isFeatured);
        container.innerHTML = featuredSchemes.map(scheme => `
            <div class="scheme-card featured" data-aos="fade-up">
                <h3>${scheme.title}</h3>
                <p>${scheme.description}</p>
                <div class="scheme-details">
                    <span class="category">${scheme.category}</span>
                    <span class="deadline">Deadline: ${this.formatDate(scheme.deadline)}</span>
                </div>
                <button class="btn btn-primary" onclick="Schemes.viewScheme(${scheme.id})">View Details</button>
            </div>
        `).join('');
    }

    renderSchemeCategories() {
        const container = document.getElementById('scheme-categories');
        if (!container) return;

        container.innerHTML = this.schemesData.categories.map(category => `
            <div class="category-card" data-aos="fade-up" onclick="Schemes.browseByCategory(${category.id})">
                <div class="category-icon"><i class="${category.icon}"></i></div>
                <h3>${category.name}</h3>
            </div>
        `).join('');
    }

    renderUserApplications() {
        const container = document.getElementById('user-applications');
        if (!container) return;

        if (!this.currentUser) {
            container.innerHTML = '<div class="empty-state">Please login to view applications</div>';
            return;
        }

        if (this.schemesData.applications.length === 0) {
            container.innerHTML = '<div class="empty-state">No applications yet</div>';
            return;
        }

        container.innerHTML = this.schemesData.applications.map(app => `
            <div class="application-card" data-aos="fade-up">
                <h3>${app.schemeTitle}</h3>
                <span class="status-badge ${app.status.toLowerCase()}">${app.status}</span>
                <p>Applied: ${this.formatDate(app.appliedDate)}</p>
            </div>
        `).join('');
    }

    renderRecentUpdates() {
        const container = document.getElementById('recent-updates');
        if (!container) return;

        container.innerHTML = this.schemesData.updates.map(update => `
            <div class="update-card" data-aos="fade-up">
                <h4>${update.title}</h4>
                <p>${update.content}</p>
                <span class="update-date">${this.formatDate(update.date)}</span>
            </div>
        `).join('');
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-search-schemes')) {
                this.showSearchModal();
            }
        });
    }

    viewScheme(schemeId) {
        const scheme = this.schemesData.schemes.find(s => s.id === schemeId);
        if (scheme) {
            this.showNotification(`Viewing scheme: ${scheme.title}`, 'info');
        }
    }

    browseByCategory(categoryId) {
        const category = this.schemesData.categories.find(c => c.id === categoryId);
        if (category) {
            this.showNotification(`Browsing ${category.name} schemes`, 'info');
        }
    }

    showSearchModal() {
        this.showNotification('Search functionality coming soon', 'info');
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

    showSchemesError(message) {
        this.showNotification(message, 'error');
    }

    static getInstance() {
        if (!window.Schemes) {
            window.Schemes = new SchemesManager();
        }
        return window.Schemes;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    SchemesManager.getInstance().init();
});

window.Schemes = SchemesManager.getInstance();
