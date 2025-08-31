// Farmazee API Integration
// Handles all communication with the Django backend

class FarmazeeAPI {
    constructor() {
        // Update baseURL to point to Django backend
        this.baseURL = 'http://localhost:8000/api';
        this.authToken = localStorage.getItem('farmazee_token');
        this.isAuthenticated = !!this.authToken;
    }

    // Authentication Methods
    async login(email, password) {
        try {
            const response = await fetch(`${this.baseURL}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            this.setAuthToken(data.token);
            this.setUserData(data.user);
            return { success: true, data };
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: error.message };
        }
    }

    async signup(userData) {
        try {
            const response = await fetch(`${this.baseURL}/auth/signup/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Signup failed');
            }

            const data = await response.json();
            this.setAuthToken(data.token);
            this.setUserData(data.user);
            return { success: true, data };
        } catch (error) {
            console.error('Signup error:', error);
            return { success: false, error: error.message };
        }
    }

    async logout() {
        try {
            if (this.authToken) {
                await fetch(`${this.baseURL}/auth/logout/`, {
                    method: 'POST',
                    headers: this.getAuthHeaders()
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.clearAuth();
        }
    }

    // User Profile Methods
    async getUserProfile() {
        try {
            const response = await this.authenticatedRequest('/users/profile/');
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async updateUserProfile(profileData) {
        try {
            const response = await this.authenticatedRequest('/users/profile/', {
                method: 'PUT',
                body: JSON.stringify(profileData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Weather Methods
    async getCurrentWeather(location) {
        try {
            const response = await this.authenticatedRequest(`/weather/current/?location=${encodeURIComponent(location)}`);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async getWeatherForecast(location, days = 7) {
        try {
            const response = await this.authenticatedRequest(`/weather/forecast/?location=${encodeURIComponent(location)}&days=${days}`);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Crop Management Methods
    async getCrops() {
        try {
            const response = await this.authenticatedRequest('/crops/');
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async createCrop(cropData) {
        try {
            const response = await this.authenticatedRequest('/crops/', {
                method: 'POST',
                body: JSON.stringify(cropData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async updateCrop(cropId, cropData) {
        try {
            const response = await this.authenticatedRequest(`/crops/${cropId}/`, {
                method: 'PUT',
                body: JSON.stringify(cropData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async deleteCrop(cropId) {
        try {
            await this.authenticatedRequest(`/crops/${cropId}/`, {
                method: 'DELETE'
            });
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Marketplace Methods
    async getProducts(category = null, search = null) {
        try {
            let url = '/marketplace/products/';
            const params = new URLSearchParams();
            if (category) params.append('category', category);
            if (search) params.append('search', search);
            if (params.toString()) url += '?' + params.toString();
            
            const response = await this.authenticatedRequest(url);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async createProduct(productData) {
        try {
            const response = await this.authenticatedRequest('/marketplace/products/', {
                method: 'POST',
                body: JSON.stringify(productData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Community Methods
    async getTopics() {
        try {
            const response = await this.authenticatedRequest('/community/topics/');
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async createTopic(topicData) {
        try {
            const response = await this.authenticatedRequest('/community/topics/', {
                method: 'POST',
                body: JSON.stringify(topicData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async getQuestions() {
        try {
            const response = await this.authenticatedRequest('/community/questions/');
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async askQuestion(questionData) {
        try {
            const response = await this.authenticatedRequest('/community/questions/', {
                method: 'POST',
                body: JSON.stringify(questionData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Government Schemes Methods
    async getSchemes(category = null) {
        try {
            let url = '/schemes/';
            if (category) url += `?category=${encodeURIComponent(category)}`;
            
            const response = await this.authenticatedRequest(url);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async applyForScheme(schemeId, applicationData) {
        try {
            const response = await this.authenticatedRequest(`/schemes/${schemeId}/apply/`, {
                method: 'POST',
                body: JSON.stringify(applicationData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Soil Health Methods
    async getSoilTests() {
        try {
            const response = await this.authenticatedRequest('/soil/tests/');
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async scheduleSoilTest(testData) {
        try {
            const response = await this.authenticatedRequest('/soil/tests/', {
                method: 'POST',
                body: JSON.stringify(testData)
            });
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async getSoilRecommendations() {
        try {
            const response = await this.authenticatedRequest('/soil/recommendations/');
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Generic API Methods
    async get(endpoint, params = {}) {
        try {
            const url = new URL(`${this.baseURL}${endpoint}`);
            Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
            
            const response = await fetch(url.toString(), {
                headers: this.getHeaders()
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('GET request error:', error);
            throw error;
        }
    }

    async post(endpoint, data = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('POST request error:', error);
            throw error;
        }
    }

    async put(endpoint, data = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('PUT request error:', error);
            throw error;
        }
    }

    async delete(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'DELETE',
                headers: this.getHeaders()
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return { success: true };
        } catch (error) {
            console.error('DELETE request error:', error);
            throw error;
        }
    }

    // Helper Methods
    async authenticatedRequest(endpoint, options = {}) {
        if (!this.isAuthenticated) {
            throw new Error('User not authenticated');
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                this.clearAuth();
                throw new Error('Authentication expired');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        return headers;
    }

    getAuthHeaders() {
        return {
            'Authorization': `Bearer ${this.authToken}`,
            'Content-Type': 'application/json',
        };
    }

    setAuthToken(token) {
        this.authToken = token;
        this.isAuthenticated = true;
        localStorage.setItem('farmazee_token', token);
    }

    setUserData(user) {
        localStorage.setItem('farmazee_user', JSON.stringify(user));
    }

    getUserData() {
        const userData = localStorage.getItem('farmazee_user');
        return userData ? JSON.parse(userData) : null;
    }

    clearAuth() {
        this.authToken = null;
        this.isAuthenticated = false;
        localStorage.removeItem('farmazee_token');
        localStorage.removeItem('farmazee_user');
    }

    // Error Handling
    handleError(error) {
        console.error('API Error:', error);
        
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            return { success: false, error: 'Network error. Please check your connection.' };
        }
        
        if (error.status === 401) {
            this.clearAuth();
            return { success: false, error: 'Authentication expired. Please login again.' };
        }
        
        if (error.status === 403) {
            return { success: false, error: 'Access denied. You do not have permission for this action.' };
        }
        
        if (error.status === 404) {
            return { success: false, error: 'Resource not found.' };
        }
        
        if (error.status >= 500) {
            return { success: false, error: 'Server error. Please try again later.' };
        }
        
        return { success: false, error: error.message || 'An unexpected error occurred.' };
    }
}

// Initialize API instance
const farmazeeAPI = new FarmazeeAPI();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FarmazeeAPI;
}
