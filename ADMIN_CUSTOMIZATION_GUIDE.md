# Farmazee Admin Panel - Complete Customization Guide

## Overview
The Farmazee admin panel now provides comprehensive customization capabilities, allowing administrators to control every aspect of the application without touching code. This guide covers all available customization options.

## 🚀 Getting Started

### Accessing the Admin Panel
1. Navigate to `/admin-panel/` (requires admin privileges)
2. Use the "System Settings" section for customization
3. All changes are applied immediately

### Initial Setup
```bash
# Create admin user (if not exists)
python manage.py create_admin_user

# Initialize system settings
python manage.py init_system_settings
```

## 🎨 UI/UX Customization

### Color Scheme
- **Primary Color**: Main brand color for buttons, links, and highlights
- **Secondary Color**: Secondary elements and borders
- **Accent Color**: Success states and call-to-action elements

### Typography
- **Font Family**: Choose from Inter, Roboto, Open Sans, Lato, or Poppins
- **Theme Support**: Light, Dark, or Auto (system preference)
- **Dark Mode**: Enable/disable dark mode option for users

### Dynamic Styling
- Colors automatically apply to Bootstrap components
- CSS variables update in real-time
- Responsive design maintained across all devices

## 📝 Content Customization

### Site Identity
- **Site Name**: Change "Farmazee" to your brand
- **Site Description**: Update meta description and branding
- **Homepage Title**: Customize main page heading
- **Homepage Subtitle**: Update tagline and description

### Page Content
- **About Page**: Full control over about page content
- **Contact Page**: Customize contact information and messaging
- **Footer Text**: Update copyright and footer information

### Legal Pages
- **Terms of Service**: Customize terms and conditions
- **Privacy Policy**: Update privacy policy content
- **Cookie Policy**: Manage cookie consent information

## 🔧 Feature Toggles

### Core Features
- **Marketplace**: Enable/disable e-commerce functionality
- **Community**: Control forum and social features
- **AI Chatbot**: Toggle AI assistant availability
- **Weather**: Enable/disable weather forecasting
- **Soil Health**: Control soil analysis features
- **Crop Planning**: Toggle crop management tools
- **Government Schemes**: Enable/disable scheme information

### Benefits
- Hide features not relevant to your region
- Control access based on subscription tiers
- A/B test feature adoption
- Reduce complexity for specific user groups

## 🔍 SEO & Analytics

### Meta Information
- **Meta Title**: Customize page titles (max 60 characters)
- **Meta Description**: Update descriptions (max 160 characters)
- **Meta Keywords**: Add relevant keywords for search engines

### Analytics Integration
- **Google Analytics**: Add GA4 tracking ID
- **Facebook Pixel**: Enable Facebook advertising tracking
- **Custom Tracking**: Support for additional analytics platforms

### Social Media
- **Facebook**: Add Facebook page URL
- **Twitter**: Include Twitter profile
- **Instagram**: Link Instagram account
- **YouTube**: Add YouTube channel
- **LinkedIn**: Include company LinkedIn

## 📧 Email & Notifications

### SMTP Configuration
- **SMTP Host**: Configure email server (Gmail, Outlook, etc.)
- **SMTP Port**: Set appropriate port (587 for TLS, 465 for SSL)
- **Authentication**: Username and password for email server
- **From Address**: Customize sender email and name

### Notification Settings
- **Email Notifications**: Enable/disable email alerts
- **SMS Notifications**: Toggle SMS functionality
- **Push Notifications**: Control push notification delivery
- **Admin Alerts**: Manage administrative notifications

## 🔒 Security & Authentication

### Session Management
- **Session Timeout**: Configure user session duration (15-1440 minutes)
- **Login Attempts**: Set maximum failed login attempts (3-10)
- **Password Policy**: Minimum length and complexity requirements
- **Two-Factor Authentication**: Enable 2FA for admin users

### Security Features
- **CSRF Protection**: Enable/disable CSRF token validation
- **Allowed Hosts**: Configure permitted domain names
- **Strong Passwords**: Enforce password complexity rules

## 💾 Backup & Maintenance

### Automated Backups
- **Auto Backup**: Enable automatic database backups
- **Frequency**: Daily, weekly, or monthly backups
- **Retention**: Configure backup retention period (7-365 days)
- **Location**: Set backup storage directory

### Manual Operations
- **Create Backup**: Generate immediate backup
- **View History**: Access backup logs and history
- **Maintenance Mode**: Enable site maintenance with custom message

## 🔌 Third-Party Integrations

### API Keys
- **OpenRouter**: AI chatbot functionality
- **Weather API**: Weather data and forecasts
- **Google Maps**: Location services and mapping
- **Payment Gateway**: Choose between Razorpay, Stripe, or PayPal

### Testing
- **Email Connection**: Test SMTP configuration
- **Integration Tests**: Verify API key validity
- **Connection Status**: Monitor integration health

## ⚡ Performance Optimization

### Caching
- **Enable Caching**: Turn on page and data caching
- **Cache Timeout**: Set cache duration (60-3600 seconds)
- **Compression**: Enable GZIP compression
- **Minification**: Minify CSS and JavaScript files

### Optimization
- **Asset Optimization**: Automatic asset compression
- **Database Optimization**: Query optimization and indexing
- **CDN Support**: Content delivery network integration

## 🌍 Localization

### Language Support
- **Primary Language**: Set default language
- **Supported Languages**: English, Hindi, Telugu, Tamil
- **Timezone**: Configure server timezone
- **Date Formats**: Localized date and time display

### Regional Settings
- **Currency**: Set local currency for marketplace
- **Units**: Configure measurement units (metric/imperial)
- **Local Content**: Region-specific information and schemes

## 📱 Mobile & Responsiveness

### Mobile Optimization
- **Responsive Design**: Automatic mobile adaptation
- **Touch Support**: Mobile-friendly navigation
- **Progressive Web App**: PWA capabilities
- **Offline Support**: Basic offline functionality

## 🔄 Real-Time Updates

### Live Customization
- **Instant Preview**: See changes immediately
- **No Restart Required**: Changes apply without server restart
- **User Experience**: Seamless updates for all users
- **Version Control**: Track setting changes over time

## 📊 Monitoring & Analytics

### System Health
- **Performance Metrics**: Monitor response times
- **Error Tracking**: Log and track system errors
- **User Analytics**: Track feature usage and adoption
- **System Resources**: Monitor server performance

## 🛠️ Advanced Features

### Custom CSS/JS
- **Custom Styling**: Add custom CSS rules
- **JavaScript Extensions**: Include custom JavaScript
- **Theme Overrides**: Override default Bootstrap styles
- **Responsive Breakpoints**: Custom mobile breakpoints

### Database Management
- **Data Export**: Export user and content data
- **Import Tools**: Bulk import functionality
- **Data Cleanup**: Remove outdated or invalid data
- **Backup Verification**: Validate backup integrity

## 📋 Best Practices

### Organization
1. **Group Related Settings**: Use logical grouping for related options
2. **Document Changes**: Keep track of setting modifications
3. **Test Changes**: Verify settings in staging environment
4. **Backup Before Changes**: Create backup before major modifications

### Performance
1. **Optimize Images**: Use appropriate image sizes and formats
2. **Minimize HTTP Requests**: Combine CSS/JS files
3. **Enable Caching**: Use appropriate cache settings
4. **Monitor Performance**: Track page load times

### Security
1. **Regular Updates**: Keep API keys and credentials current
2. **Access Control**: Limit admin access to trusted users
3. **Audit Logs**: Monitor setting changes and access
4. **Secure Storage**: Use environment variables for sensitive data

## 🚨 Troubleshooting

### Common Issues
- **Settings Not Saving**: Check CSRF token and form submission
- **Changes Not Visible**: Clear browser cache and refresh
- **Performance Issues**: Review caching and optimization settings
- **Email Not Working**: Verify SMTP configuration and credentials

### Debug Mode
- Enable debug mode for detailed error messages
- Check Django logs for specific error details
- Verify database connectivity and permissions
- Test individual features in isolation

## 📚 API Reference

### Settings Endpoints
- `GET /admin-panel/system-settings/` - View current settings
- `POST /admin-panel/system-settings/` - Update settings
- `POST /admin-panel/system-settings/reset/` - Reset to defaults

### Response Format
```json
{
    "success": true,
    "message": "Settings updated successfully",
    "data": {
        "site_name": "Updated Site Name",
        "primary_color": "#007bff"
    }
}
```

## 🔮 Future Enhancements

### Planned Features
- **Multi-tenant Support**: Multiple site configurations
- **Advanced Theming**: Custom theme builder
- **A/B Testing**: Built-in testing framework
- **Advanced Analytics**: Detailed user behavior tracking
- **API Management**: RESTful API for external integrations

### Custom Development
- **Plugin System**: Extend functionality with plugins
- **Custom Fields**: Add site-specific configuration options
- **Workflow Automation**: Automated setting management
- **Integration Hub**: Centralized third-party service management

## 📞 Support

### Getting Help
- **Documentation**: Refer to this guide for common tasks
- **Admin Panel**: Use built-in help and tooltips
- **Community**: Join our developer community
- **Support Team**: Contact support for technical issues

### Contributing
- **Feature Requests**: Submit enhancement ideas
- **Bug Reports**: Report issues with detailed information
- **Code Contributions**: Contribute to open-source development
- **Documentation**: Help improve guides and tutorials

---

**Note**: This admin panel provides enterprise-level customization capabilities. All changes are applied in real-time and affect the entire application. Always test changes in a staging environment before applying to production.
