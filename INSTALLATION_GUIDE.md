# 🚀 Farmazee Installation Guide

## Quick Start (Recommended)

### 1. Install Minimal Requirements
```bash
pip install -r requirements-minimal.txt
```

### 2. If that works, install full requirements
```bash
pip install -r requirements.txt
```

## Troubleshooting Common Issues

### Issue: setuptools.build_meta error
**Solution**: Update pip and setuptools
```bash
python -m pip install --upgrade pip setuptools wheel
```

### Issue: Package build failures
**Solution**: Install pre-compiled wheels
```bash
pip install --only-binary=all -r requirements.txt
```

### Issue: Python version compatibility
**Solution**: Use Python 3.8-3.11 for best compatibility
```bash
# Check your Python version
python --version

# If using Python 3.13+, some packages may need updates
```

## Alternative Installation Methods

### Method 1: Install packages one by one
```bash
pip install Django
pip install djangorestframework
pip install django-cors-headers
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install Pillow
pip install python-decouple
pip install python-dotenv
pip install requests
```

### Method 2: Use conda (if available)
```bash
conda install django djangorestframework pillow requests
conda install -c conda-forge django-cors-headers django-crispy-forms
```

### Method 3: Virtual environment with specific Python version
```bash
# Create virtual environment with Python 3.11
python3.11 -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install packages
pip install -r requirements-minimal.txt
```

## What Each Package Does

- **Django**: Web framework
- **djangorestframework**: API framework
- **django-cors-headers**: Handle cross-origin requests
- **django-crispy-forms**: Better form rendering
- **crispy-bootstrap5**: Bootstrap 5 styling for forms
- **Pillow**: Image processing
- **python-decouple**: Environment variable management
- **python-dotenv**: Load .env files
- **requests**: HTTP library for API calls

## After Installation

1. **Set up environment**:
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create admin user**:
   ```bash
   python manage.py create_admin_user
   ```

4. **Start server**:
   ```bash
   python manage.py runserver
   ```

## Need Help?

- Check Python version: `python --version`
- Check pip version: `pip --version`
- Try installing with verbose output: `pip install -v package_name`
- Check for conflicting packages: `pip list`

---

## 📚 **Want to Learn More?**

### 🚀 **Get Started:**
- **[README_SIMPLE.md](README_SIMPLE.md)** - Super simple explanation for beginners
- **[STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md)** - Follow step-by-step setup
- **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - See diagrams and flowcharts

### 🔧 **Technical Help:**
- **[TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)** - Fix any problem
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Guide to all documentation

### 📖 **Complete Documentation:**
- **[README.md](README.md)** - Full technical documentation
