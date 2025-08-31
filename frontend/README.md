# Farmazee Frontend 🚀

A modern, responsive frontend for the **Farmazee** smart farming platform built with vanilla HTML, CSS, and JavaScript. This frontend provides a comprehensive user interface for all farming-related features including weather monitoring, crop management, marketplace, community forums, government schemes, and soil health monitoring.

## 🌟 Features

### Core Features
- **Modern Landing Page** - Professional hero section with clear value proposition
- **Responsive Design** - Mobile-first approach with cross-device compatibility
- **Authentication System** - Secure login/signup with JWT token management
- **Dashboard Interface** - Comprehensive dashboard with multiple modules
- **Real-time Updates** - Live data updates and notifications

### Smart Farming Modules
- **Weather Management** - Current weather, forecasts, alerts, and maps
- **Crop Management** - Crop tracking, activities, health monitoring
- **Marketplace** - Product browsing, cart management, orders
- **Community Features** - Forums, Q&A, expert consultations, events
- **Government Schemes** - Scheme browsing, applications, updates
- **Soil Health** - Soil testing, monitoring, recommendations, alerts

### Technical Features
- **Modular Architecture** - Clean separation of concerns
- **API Integration** - Ready for Django backend integration
- **Local Storage** - User session management
- **Error Handling** - Comprehensive error management
- **Performance Optimized** - Lazy loading and efficient rendering

## 🏗️ Architecture

```
frontend/
├── index.html              # Main entry point
├── css/
│   ├── style.css          # Global styles and layout
│   ├── components.css     # Component-specific styles
│   └── responsive.css     # Responsive design & media queries
├── js/
│   ├── config.js          # Configuration and branding
│   ├── api.js             # API integration layer
│   ├── main.js            # Core application logic
│   ├── auth.js            # Authentication management
│   ├── dashboard.js       # Dashboard functionality
│   ├── weather.js         # Weather features
│   ├── crops.js           # Crop management
│   ├── marketplace.js     # Marketplace features
│   ├── community.js       # Community & forums
│   ├── schemes.js         # Government schemes
│   └── soil-health.js     # Soil health management
└── assets/
    └── images/            # Image assets (to be added)
```

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (optional, for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/farmazee.git
   cd farmazee/frontend
   ```

2. **Open in browser**
   - Simply open `index.html` in any modern browser
   - Or use a local server for development

3. **Local Development Server** (Optional)
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8000
   ```

4. **Access the application**
   - Open `http://localhost:8000` in your browser

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GA_TRACKING_ID=your-ga-tracking-id

# Feature Flags
REACT_APP_ENABLE_OFFLINE_MODE=false
REACT_APP_ENABLE_ANALYTICS=true
```

### Branding Customization
Update `js/config.js` to customize:
- Brand colors and theme
- Company information
- Feature flags
- API endpoints
- Localization settings

## 🔌 Backend Integration

### API Endpoints
The frontend is configured to work with the Django backend API:

- **Authentication**: `/api/auth/login/`, `/api/auth/signup/`
- **Weather**: `/api/weather/current/`, `/api/weather/forecast/`
- **Crops**: `/api/crops/user-crops/`, `/api/crops/add/`
- **Marketplace**: `/api/marketplace/products/`, `/api/marketplace/cart/`
- **Community**: `/api/community/topics/`, `/api/community/questions/`
- **Schemes**: `/api/schemes/list/`, `/api/schemes/apply/`
- **Soil Health**: `/api/soil-health/tests/`, `/api/soil-health/recommendations/`

### Integration Steps
1. **Update API Base URL** in `js/config.js`
2. **Configure CORS** on your Django backend
3. **Set up authentication** endpoints
4. **Test API connectivity** using the health check

## 🎨 Customization

### Styling
- **Colors**: Update CSS variables in `css/style.css`
- **Typography**: Modify font families and sizes
- **Layout**: Adjust grid systems and spacing
- **Components**: Customize component styles in `css/components.css`

### Content
- **Branding**: Update company name, logo, and contact information
- **Images**: Replace placeholder content with actual images
- **Text**: Customize all text content for your region/audience
- **Features**: Enable/disable features in `js/config.js`

### Functionality
- **Modules**: Add or remove feature modules
- **API Calls**: Modify API integration in `js/api.js`
- **Validation**: Update form validation rules
- **Notifications**: Customize notification system

## 📱 Responsive Design

The frontend is built with a mobile-first approach:

- **Breakpoints**: 320px, 576px, 768px, 992px, 1200px
- **Touch Optimized**: Touch-friendly buttons and interactions
- **Performance**: Optimized for mobile devices
- **Accessibility**: WCAG compliant design patterns

## 🌐 Browser Support

- **Chrome**: 80+
- **Firefox**: 75+
- **Safari**: 13+
- **Edge**: 80+
- **Mobile Browsers**: iOS Safari 13+, Chrome Mobile 80+

## 🧪 Testing

### Manual Testing
1. **Cross-browser testing** on different browsers
2. **Responsive testing** on various device sizes
3. **Functionality testing** of all features
4. **Performance testing** with browser dev tools

### Automated Testing
```bash
# Run accessibility tests
npm run test:a11y

# Run performance tests
npm run test:performance

# Run cross-browser tests
npm run test:browser
```

## 📦 Deployment

### Production Build
1. **Optimize assets** (minify CSS/JS, compress images)
2. **Update configuration** for production environment
3. **Set up CDN** for static assets
4. **Configure caching** headers

### Deployment Options
- **Static Hosting**: Netlify, Vercel, GitHub Pages
- **Cloud Storage**: AWS S3, Google Cloud Storage
- **Traditional Hosting**: Apache, Nginx
- **CDN**: Cloudflare, AWS CloudFront

## 🔒 Security

- **HTTPS Only**: Enforce secure connections
- **CSP Headers**: Content Security Policy
- **XSS Protection**: Input sanitization
- **CSRF Protection**: Token-based validation
- **Secure Storage**: Encrypted local storage

## 📊 Performance

- **Lazy Loading**: Images and components
- **Code Splitting**: Modular JavaScript loading
- **Caching**: Browser and service worker caching
- **Compression**: Gzip/Brotli compression
- **CDN**: Content delivery network

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Guidelines
- Follow existing code style
- Add comments for complex logic
- Update documentation
- Test on multiple devices
- Ensure accessibility compliance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [API Documentation](https://docs.farmazee.com)
- [User Guide](https://help.farmazee.com)
- [Developer Guide](https://dev.farmazee.com)

### Contact
- **Email**: support@farmazee.com
- **Phone**: +91 98765 43210
- **WhatsApp**: +91 98765 43210
- **Live Chat**: Available on website

### Community
- **Forum**: [community.farmazee.com](https://community.farmazee.com)
- **GitHub Issues**: [github.com/farmazee/frontend/issues](https://github.com/farmazee/frontend/issues)
- **Discord**: [discord.gg/farmazee](https://discord.gg/farmazee)

## 🙏 Acknowledgments

- **Farmers** - For inspiring this platform
- **Open Source Community** - For amazing tools and libraries
- **Design Team** - For beautiful UI/UX
- **Development Team** - For robust implementation

---

**Made with ❤️ by the Farmazee Team**

*Empowering farmers with technology for a sustainable future*
