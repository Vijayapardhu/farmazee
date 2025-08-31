// Community Management for Farmazee
// Handles community features, forums, Q&A, expert consultations, and events

class CommunityManager {
    constructor() {
        this.communityData = {
            topics: [],
            questions: [],
            experts: [],
            events: [],
            discussions: [],
            polls: []
        };
        this.currentUser = null;
        this.isInitialized = false;
    }

    init() {
        if (this.isInitialized) return;
        
        this.currentUser = this.getCurrentUser();
        this.loadCommunityData();
        this.setupEventListeners();
        this.isInitialized = true;
        
        console.log('Community Manager initialized');
    }

    getCurrentUser() {
        const userStr = localStorage.getItem('farmazee_user');
        return userStr ? JSON.parse(userStr) : null;
    }

    async loadCommunityData() {
        try {
            await Promise.all([
                this.loadTopics(),
                this.loadQuestions(),
                this.loadExperts(),
                this.loadEvents(),
                this.loadDiscussions(),
                this.loadPolls()
            ]);
            
            this.renderCommunityData();
        } catch (error) {
            console.error('Error loading community data:', error);
            this.showCommunityError('Failed to load community data');
        }
    }

    async loadTopics() {
        // Simulate API call
        this.communityData.topics = [
            {
                id: 1,
                title: 'Organic Farming Techniques',
                description: 'Share your experiences with organic farming methods',
                category: 'Farming Methods',
                postCount: 45,
                lastActivity: '2025-01-15T10:30:00Z',
                isActive: true
            },
            {
                id: 2,
                title: 'Crop Disease Management',
                description: 'Discuss common crop diseases and prevention methods',
                category: 'Crop Health',
                postCount: 32,
                lastActivity: '2025-01-14T15:45:00Z',
                isActive: true
            },
            {
                id: 3,
                title: 'Market Trends & Prices',
                description: 'Latest updates on agricultural market trends',
                category: 'Market',
                postCount: 28,
                lastActivity: '2025-01-13T09:20:00Z',
                isActive: true
            },
            {
                id: 4,
                title: 'Government Schemes',
                description: 'Information about agricultural subsidies and schemes',
                category: 'Schemes',
                postCount: 19,
                lastActivity: '2025-01-12T14:15:00Z',
                isActive: true
            }
        ];
    }

    async loadQuestions() {
        // Simulate API call
        this.communityData.questions = [
            {
                id: 1,
                title: 'Best time to plant tomatoes in Telangana?',
                content: 'I\'m planning to grow tomatoes this season. What\'s the ideal planting time and any specific tips for Telangana climate?',
                author: 'Farmer_Raju',
                category: 'Crop Management',
                tags: ['tomatoes', 'planting', 'telangana'],
                answers: 8,
                views: 156,
                isSolved: false,
                createdAt: '2025-01-15T08:00:00Z'
            },
            {
                id: 2,
                title: 'How to control aphids naturally?',
                content: 'My cotton crop is being attacked by aphids. Looking for natural and organic methods to control them.',
                author: 'Organic_Farmer',
                category: 'Pest Control',
                tags: ['aphids', 'cotton', 'organic', 'pest-control'],
                answers: 12,
                views: 234,
                isSolved: true,
                createdAt: '2025-01-14T12:30:00Z'
            },
            {
                id: 3,
                title: 'Soil testing recommendations near Hyderabad',
                content: 'Can anyone recommend a good soil testing lab near Hyderabad? Also, what parameters should I test for?',
                author: 'Hyderabad_Farmer',
                category: 'Soil Health',
                tags: ['soil-testing', 'hyderabad', 'soil-health'],
                answers: 5,
                views: 89,
                isSolved: false,
                createdAt: '2025-01-13T16:45:00Z'
            }
        ];
    }

    async loadExperts() {
        // Simulate API call
        this.communityData.experts = [
            {
                id: 1,
                name: 'Dr. Rajesh Kumar',
                expertise: 'Soil Science',
                qualification: 'PhD in Agricultural Sciences',
                experience: '15+ years',
                consultationFee: 500,
                rating: 4.8,
                consultationCount: 127,
                isAvailable: true,
                avatar: './assets/images/expert-1.jpg'
            },
            {
                id: 2,
                name: 'Dr. Priya Sharma',
                expertise: 'Crop Protection',
                qualification: 'MSc in Plant Pathology',
                experience: '12+ years',
                consultationFee: 400,
                rating: 4.9,
                consultationCount: 98,
                isAvailable: true,
                avatar: './assets/images/expert-2.jpg'
            },
            {
                id: 3,
                name: 'Krishna Reddy',
                expertise: 'Organic Farming',
                qualification: 'BSc in Agriculture',
                experience: '20+ years',
                consultationFee: 300,
                rating: 4.7,
                consultationCount: 156,
                isAvailable: false,
                avatar: './assets/images/expert-3.jpg'
            }
        ];
    }

    async loadEvents() {
        // Simulate API call
        this.communityData.events = [
            {
                id: 1,
                title: 'Organic Farming Workshop',
                description: 'Learn practical organic farming techniques from experts',
                eventDate: '2025-02-15T09:00:00Z',
                duration: '6 hours',
                location: 'Hyderabad Agricultural University',
                eventType: 'workshop',
                isFree: false,
                feeAmount: 1000,
                registrationDeadline: '2025-02-10T23:59:59Z',
                maxParticipants: 50,
                currentParticipants: 35,
                isRegistrationOpen: true
            },
            {
                id: 2,
                title: 'Crop Disease Management Seminar',
                description: 'Comprehensive seminar on identifying and managing crop diseases',
                eventDate: '2025-02-20T14:00:00Z',
                duration: '4 hours',
                location: 'Online (Zoom)',
                eventType: 'seminar',
                isFree: true,
                feeAmount: 0,
                registrationDeadline: '2025-02-19T23:59:59Z',
                maxParticipants: 200,
                currentParticipants: 156,
                isRegistrationOpen: true
            },
            {
                id: 3,
                title: 'Farmers Meet & Networking',
                description: 'Annual gathering of farmers to share experiences and network',
                eventDate: '2025-03-01T10:00:00Z',
                duration: '8 hours',
                location: 'Telangana State Agricultural Complex',
                eventType: 'networking',
                isFree: true,
                feeAmount: 0,
                registrationDeadline: '2025-02-25T23:59:59Z',
                maxParticipants: 300,
                currentParticipants: 245,
                isRegistrationOpen: true
            }
        ];
    }

    async loadDiscussions() {
        // Simulate API call
        this.communityData.discussions = [
            {
                id: 1,
                topic: 'Water Conservation in Farming',
                author: 'Water_Saver',
                content: 'What are the most effective water conservation methods you\'ve used in your farming?',
                replies: 23,
                likes: 45,
                createdAt: '2025-01-15T07:30:00Z'
            },
            {
                id: 2,
                topic: 'Success with Vertical Farming',
                author: 'Vertical_Grower',
                content: 'I\'ve been experimenting with vertical farming for vegetables. Great results so far!',
                replies: 18,
                likes: 32,
                createdAt: '2025-01-14T14:20:00Z'
            }
        ];
    }

    async loadPolls() {
        // Simulate API call
        this.communityData.polls = [
            {
                id: 1,
                question: 'Which crop gives you the best profit margin?',
                options: [
                    { id: 1, text: 'Cotton', votes: 45 },
                    { id: 2, text: 'Rice', votes: 32 },
                    { id: 3, text: 'Vegetables', votes: 67 },
                    { id: 4, text: 'Pulses', votes: 28 }
                ],
                totalVotes: 172,
                isActive: true,
                endDate: '2025-02-15T23:59:59Z',
                createdBy: 'Community_Admin'
            },
            {
                id: 2,
                question: 'What\'s your biggest farming challenge?',
                options: [
                    { id: 1, text: 'Weather uncertainty', votes: 89 },
                    { id: 2, text: 'Market price fluctuations', votes: 67 },
                    { id: 3, text: 'Pest and disease management', votes: 54 },
                    { id: 4, text: 'Access to credit', votes: 43 }
                ],
                totalVotes: 253,
                isActive: true,
                endDate: '2025-02-20T23:59:59Z',
                createdBy: 'Community_Admin'
            }
        ];
    }

    renderCommunityData() {
        this.renderTopics();
        this.renderQuestions();
        this.renderExperts();
        this.renderEvents();
        this.renderDiscussions();
        this.renderPolls();
    }

    renderTopics() {
        const topicsContainer = document.getElementById('community-topics');
        if (!topicsContainer) return;

        const topicsHTML = this.communityData.topics.map(topic => `
            <div class="community-card" data-aos="fade-up">
                <div class="card-header">
                    <h3>${topic.title}</h3>
                    <span class="category-badge">${topic.category}</span>
                </div>
                <p>${topic.description}</p>
                <div class="card-stats">
                    <span><i class="fas fa-comments"></i> ${topic.postCount} posts</span>
                    <span><i class="fas fa-clock"></i> ${this.formatTimeAgo(topic.lastActivity)}</span>
                </div>
                <button class="btn btn-secondary" onclick="Community.viewTopic(${topic.id})">
                    Join Discussion
                </button>
            </div>
        `).join('');

        topicsContainer.innerHTML = topicsHTML;
    }

    renderQuestions() {
        const questionsContainer = document.getElementById('community-questions');
        if (!questionsContainer) return;

        const questionsHTML = this.communityData.questions.map(question => `
            <div class="community-card question-card" data-aos="fade-up">
                <div class="question-header">
                    <h3>${question.title}</h3>
                    ${question.isSolved ? '<span class="solved-badge">Solved</span>' : ''}
                </div>
                <p class="question-content">${question.content}</p>
                <div class="question-meta">
                    <span class="author">By ${question.author}</span>
                    <span class="category">${question.category}</span>
                </div>
                <div class="question-stats">
                    <span><i class="fas fa-comments"></i> ${question.answers} answers</span>
                    <span><i class="fas fa-eye"></i> ${question.views} views</span>
                    <span><i class="fas fa-clock"></i> ${this.formatTimeAgo(question.createdAt)}</span>
                </div>
                <div class="question-tags">
                    ${question.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
                <button class="btn btn-primary" onclick="Community.viewQuestion(${question.id})">
                    View Answers
                </button>
            </div>
        `).join('');

        questionsContainer.innerHTML = questionsHTML;
    }

    renderExperts() {
        const expertsContainer = document.getElementById('community-experts');
        if (!expertsContainer) return;

        const expertsHTML = this.communityData.experts.map(expert => `
            <div class="community-card expert-card" data-aos="fade-up">
                <div class="expert-header">
                    <img src="${expert.avatar}" alt="${expert.name}" class="expert-avatar">
                    <div class="expert-info">
                        <h3>${expert.name}</h3>
                        <p class="expertise">${expert.expertise}</p>
                        <div class="expert-rating">
                            ${this.generateStarRating(expert.rating)}
                            <span class="rating-text">${expert.rating}/5</span>
                        </div>
                    </div>
                </div>
                <div class="expert-details">
                    <p><strong>Qualification:</strong> ${expert.qualification}</p>
                    <p><strong>Experience:</strong> ${expert.experience}</p>
                    <p><strong>Consultations:</strong> ${expert.consultationCount}</p>
                </div>
                <div class="expert-actions">
                    <span class="consultation-fee">₹${expert.consultationFee}/session</span>
                    <button class="btn btn-primary" onclick="Community.bookConsultation(${expert.id})" 
                            ${!expert.isAvailable ? 'disabled' : ''}>
                        ${expert.isAvailable ? 'Book Consultation' : 'Not Available'}
                    </button>
                </div>
            </div>
        `).join('');

        expertsContainer.innerHTML = expertsHTML;
    }

    renderEvents() {
        const eventsContainer = document.getElementById('community-events');
        if (!eventsContainer) return;

        const eventsHTML = this.communityData.events.map(event => `
            <div class="community-card event-card" data-aos="fade-up">
                <div class="event-header">
                    <h3>${event.title}</h3>
                    <span class="event-type-badge">${event.eventType}</span>
                </div>
                <p class="event-description">${event.description}</p>
                <div class="event-details">
                    <div class="event-info">
                        <span><i class="fas fa-calendar"></i> ${this.formatDate(event.eventDate)}</span>
                        <span><i class="fas fa-clock"></i> ${event.duration}</span>
                        <span><i class="fas fa-map-marker-alt"></i> ${event.location}</span>
                    </div>
                    <div class="event-pricing">
                        <span class="fee">
                            ${event.isFree ? 'Free' : `₹${event.feeAmount}`}
                        </span>
                    </div>
                </div>
                <div class="event-registration">
                    <div class="registration-stats">
                        <span>${event.currentParticipants}/${event.maxParticipants} registered</span>
                        <span class="deadline">Deadline: ${this.formatDate(event.registrationDeadline)}</span>
                    </div>
                    <button class="btn btn-primary" onclick="Community.registerEvent(${event.id})"
                            ${!event.isRegistrationOpen ? 'disabled' : ''}>
                        ${event.isRegistrationOpen ? 'Register Now' : 'Registration Closed'}
                    </button>
                </div>
            </div>
        `).join('');

        eventsContainer.innerHTML = eventsHTML;
    }

    renderDiscussions() {
        const discussionsContainer = document.getElementById('community-discussions');
        if (!discussionsContainer) return;

        const discussionsHTML = this.communityData.discussions.map(discussion => `
            <div class="community-card discussion-card" data-aos="fade-up">
                <div class="discussion-header">
                    <h3>${discussion.topic}</h3>
                    <span class="author">By ${discussion.author}</span>
                </div>
                <p class="discussion-content">${discussion.content}</p>
                <div class="discussion-stats">
                    <span><i class="fas fa-comments"></i> ${discussion.replies} replies</span>
                    <span><i class="fas fa-thumbs-up"></i> ${discussion.likes} likes</span>
                    <span><i class="fas fa-clock"></i> ${this.formatTimeAgo(discussion.createdAt)}</span>
                </div>
                <button class="btn btn-secondary" onclick="Community.joinDiscussion(${discussion.id})">
                    Join Discussion
                </button>
            </div>
        `).join('');

        discussionsContainer.innerHTML = discussionsHTML;
    }

    renderPolls() {
        const pollsContainer = document.getElementById('community-polls');
        if (!pollsContainer) return;

        const pollsHTML = this.communityData.polls.map(poll => `
            <div class="community-card poll-card" data-aos="fade-up">
                <div class="poll-header">
                    <h3>${poll.question}</h3>
                    <span class="poll-status ${poll.isActive ? 'active' : 'closed'}">
                        ${poll.isActive ? 'Active' : 'Closed'}
                    </span>
                </div>
                <div class="poll-options">
                    ${poll.options.map(option => {
                        const percentage = poll.totalVotes > 0 ? Math.round((option.votes / poll.totalVotes) * 100) : 0;
                        return `
                            <div class="poll-option" onclick="Community.voteInPoll(${poll.id}, ${option.id})">
                                <div class="option-bar">
                                    <div class="option-fill" style="width: ${percentage}%"></div>
                                </div>
                                <span class="option-text">${option.text}</span>
                                <span class="option-votes">${option.votes} votes (${percentage}%)</span>
                            </div>
                        `;
                    }).join('')}
                </div>
                <div class="poll-footer">
                    <span class="total-votes">Total: ${poll.totalVotes} votes</span>
                    <span class="poll-end">Ends: ${this.formatDate(poll.endDate)}</span>
                </div>
            </div>
        `).join('');

        pollsContainer.innerHTML = pollsHTML;
    }

    setupEventListeners() {
        // Add event listeners for community interactions
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-ask-question')) {
                this.showAskQuestionModal();
            }
            if (e.target.matches('.btn-create-topic')) {
                this.showCreateTopicModal();
            }
        });
    }

    // Community Actions
    viewTopic(topicId) {
        const topic = this.communityData.topics.find(t => t.id === topicId);
        if (topic) {
            this.showNotification(`Opening topic: ${topic.title}`, 'info');
            // In a real app, this would navigate to the topic page
        }
    }

    viewQuestion(questionId) {
        const question = this.communityData.questions.find(q => q.id === questionId);
        if (question) {
            this.showNotification(`Opening question: ${question.title}`, 'info');
            // In a real app, this would navigate to the question page
        }
    }

    bookConsultation(expertId) {
        const expert = this.communityData.experts.find(e => e.id === expertId);
        if (expert && this.currentUser) {
            this.showNotification(`Booking consultation with ${expert.name}`, 'success');
            // In a real app, this would open a booking form
        } else if (!this.currentUser) {
            this.showNotification('Please login to book consultations', 'warning');
        }
    }

    registerEvent(eventId) {
        const event = this.communityData.events.find(e => e.id === eventId);
        if (event && this.currentUser) {
            if (event.currentParticipants < event.maxParticipants) {
                this.showNotification(`Registered for: ${event.title}`, 'success');
                // In a real app, this would update the registration count
            } else {
                this.showNotification('Event is full', 'warning');
            }
        } else if (!this.currentUser) {
            this.showNotification('Please login to register for events', 'warning');
        }
    }

    joinDiscussion(discussionId) {
        const discussion = this.communityData.discussions.find(d => d.id === discussionId);
        if (discussion) {
            this.showNotification(`Joining discussion: ${discussion.topic}`, 'info');
            // In a real app, this would navigate to the discussion page
        }
    }

    voteInPoll(pollId, optionId) {
        if (this.currentUser) {
            this.showNotification('Vote recorded successfully!', 'success');
            // In a real app, this would update the poll results
        } else {
            this.showNotification('Please login to vote in polls', 'warning');
        }
    }

    showAskQuestionModal() {
        if (!this.currentUser) {
            this.showNotification('Please login to ask questions', 'warning');
            return;
        }

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Ask a Question</h2>
                <form id="ask-question-form" class="auth-form">
                    <div class="form-group">
                        <input type="text" id="question-title" placeholder="Question Title" required>
                    </div>
                    <div class="form-group">
                        <textarea id="question-content" placeholder="Describe your question in detail..." rows="5" required></textarea>
                    </div>
                    <div class="form-group">
                        <select id="question-category" required>
                            <option value="">Select Category</option>
                            <option value="Crop Management">Crop Management</option>
                            <option value="Soil Health">Soil Health</option>
                            <option value="Pest Control">Pest Control</option>
                            <option value="Market">Market</option>
                            <option value="Schemes">Government Schemes</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <input type="text" id="question-tags" placeholder="Tags (comma separated)">
                    </div>
                    <button type="submit" class="btn btn-primary btn-full">Ask Question</button>
                </form>
            </div>
        `;

        document.body.appendChild(modal);
        this.setupModalEventListeners(modal);
    }

    showCreateTopicModal() {
        if (!this.currentUser) {
            this.showNotification('Please login to create topics', 'warning');
            return;
        }

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Create New Topic</h2>
                <form id="create-topic-form" class="auth-form">
                    <div class="form-group">
                        <input type="text" id="topic-title" placeholder="Topic Title" required>
                    </div>
                    <div class="form-group">
                        <textarea id="topic-description" placeholder="Topic Description..." rows="4" required></textarea>
                    </div>
                    <div class="form-group">
                        <select id="topic-category" required>
                            <option value="">Select Category</option>
                            <option value="Farming Methods">Farming Methods</option>
                            <option value="Crop Health">Crop Health</option>
                            <option value="Market">Market</option>
                            <option value="Schemes">Government Schemes</option>
                            <option value="Technology">Technology</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary btn-full">Create Topic</button>
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

        form.onsubmit = (e) => {
            e.preventDefault();
            this.handleFormSubmission(form, modal);
        };
    }

    handleFormSubmission(form, modal) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Simulate API call
        setTimeout(() => {
            this.showNotification('Submitted successfully!', 'success');
            modal.remove();
            // In a real app, this would refresh the community data
        }, 1000);
    }

    // Utility Functions
    formatTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}d ago`;
        return date.toLocaleDateString();
    }

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

    generateStarRating(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

        let starsHTML = '';
        for (let i = 0; i < fullStars; i++) {
            starsHTML += '<i class="fas fa-star"></i>';
        }
        if (hasHalfStar) {
            starsHTML += '<i class="fas fa-star-half-alt"></i>';
        }
        for (let i = 0; i < emptyStars; i++) {
            starsHTML += '<i class="far fa-star"></i>';
        }

        return starsHTML;
    }

    showNotification(message, type = 'info') {
        if (window.Farmazee && window.Farmazee.showNotification) {
            window.Farmazee.showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }

    showCommunityError(message) {
        this.showNotification(message, 'error');
    }

    // Public API
    static getInstance() {
        if (!window.Community) {
            window.Community = new CommunityManager();
        }
        return window.Community;
    }
}

// Initialize Community Manager
document.addEventListener('DOMContentLoaded', () => {
    CommunityManager.getInstance().init();
});

// Export for global access
window.Community = CommunityManager.getInstance();

