# 🌾 Farmazee - Smart Farming Solutions

A comprehensive Django-based platform providing smart farming solutions, crop management, weather forecasting, and agricultural tools for modern farmers.

## 🚀 Features

### Core Functionality
- **Crop Management**: Plan, track, and manage crops with AI-powered recommendations
- **Weather Integration**: Real-time weather forecasts and alerts
- **Soil Health Monitoring**: Soil analysis and improvement recommendations
- **Marketplace**: E-commerce platform for agricultural inputs and products
- **Community**: Farmer forums and knowledge sharing
- **AI Chatbot**: Intelligent farming assistant
- **Government Schemes**: Information about agricultural subsidies and schemes

### Admin Panel
- **Complete Customization**: Control every aspect of the application through admin interface
- **Feature Toggles**: Enable/disable features without code changes
- **Dynamic Styling**: Real-time color scheme and theme customization
- **Content Management**: Update site content, legal pages, and branding
- **SEO Management**: Meta tags, analytics, and social media integration

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7, Python 3.8+
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI/ML**: OpenCV, scikit-learn, pandas, numpy
- **Real-time**: Django Channels, WebSockets
- **Background Tasks**: Celery, Redis
- **Authentication**: Django Allauth, JWT

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Vijayapardhu/farmaazee.git
cd farmaazee
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration
# Update API keys, database settings, etc.
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User
```bash
python manage.py create_admin_user
```

### 7. Initialize System Settings
```bash
python manage.py init_system_settings
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to access the application.

## 🔧 Configuration

### Environment Variables
The application uses environment variables for configuration. Copy `env.example` to `.env` and update the values:

- **Database**: Configure database connection settings
- **API Keys**: Add your OpenRouter, Weather, and Google Maps API keys
- **Email**: Configure SMTP settings for notifications
- **Payment**: Set up payment gateway credentials
- **Analytics**: Add Google Analytics and Facebook Pixel IDs

### Admin Panel Customization
Access the admin panel at `/admin-panel/` to customize:

- **Site Identity**: Brand name, description, colors
- **Features**: Enable/disable specific functionality
- **Content**: Update legal pages, about content
- **SEO**: Meta tags, social media links
- **Performance**: Caching, compression settings

## 📱 Usage

### For Farmers
1. **Register/Login**: Create an account or sign in
2. **Crop Planning**: Plan your crops with AI recommendations
3. **Weather Check**: Get daily weather forecasts
4. **Soil Analysis**: Monitor and improve soil health
5. **Marketplace**: Buy/sell agricultural products
6. **Community**: Connect with other farmers

### For Administrators
1. **Access Admin Panel**: Navigate to `/admin-panel/`
2. **System Settings**: Customize application behavior
3. **User Management**: Manage farmer accounts
4. **Content Management**: Update site content
5. **Analytics**: Monitor platform usage

## 🏗️ Project Structure

```
farmazee/
├── core/                   # Core application (main functionality)
├── crops/                  # Crop management module
├── weather/                # Weather forecasting
├── soil_health/            # Soil analysis and monitoring
├── marketplace/            # E-commerce platform
├── community/              # Farmer community features
├── ai_chatbot/            # AI-powered farming assistant
├── schemes/                # Government schemes information
├── templates/              # HTML templates
├── static/                 # CSS, JavaScript, images
├── media/                  # User-uploaded files
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
└── README.md              # This file
```

## 🔒 Security Features

- **Authentication**: Secure user authentication with Django Allauth
- **Authorization**: Role-based access control
- **CSRF Protection**: Cross-site request forgery protection
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive form and data validation
- **SQL Injection Protection**: Django ORM protection

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Production
1. Set `DEBUG=False` in environment
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure web server (Nginx + Gunicorn)
5. Set up SSL certificates
6. Configure backup and monitoring

## 📊 API Documentation

The application provides RESTful APIs for:

- **User Management**: Registration, authentication, profiles
- **Crop Management**: CRUD operations for crops
- **Weather Data**: Current and forecast weather information
- **Marketplace**: Product and order management
- **Community**: Posts, comments, and interactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [ADMIN_CUSTOMIZATION_GUIDE.md](ADMIN_CUSTOMIZATION_GUIDE.md) for admin panel usage
- **Issues**: Report bugs and feature requests on GitHub
- **Community**: Join our developer community

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- Open source contributors for various packages

---

**Built with ❤️ for Indian Farmers**

*Farmazee - Empowering Agriculture Through Technology*
