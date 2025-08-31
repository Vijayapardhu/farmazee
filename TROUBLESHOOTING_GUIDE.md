# 🚨 Farmazee Troubleshooting Guide

## 🆘 Quick Problem Solver

### ❌ **"I can't install packages"**
**Try this first:**
```bash
python -m pip install --upgrade pip setuptools wheel
```

### ❌ **"Website won't start"**
**Try this first:**
```bash
python manage.py runserver 8001
```
Then go to: `http://localhost:8001`

### ❌ **"Can't log into admin"**
**Try this first:**
```bash
python manage.py create_admin_user
```

---

## 🔧 Installation Problems

### ❌ **Problem**: `pip is not recognized`
**What it means**: Python is not installed or not in PATH
**Solutions**:
1. **Reinstall Python**:
   - Download from [python.org](https://python.org)
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install for all users"

2. **Add Python to PATH manually**:
   - Find Python installation folder (usually `C:\Python311`)
   - Add to Windows PATH environment variable

3. **Use full path**:
   ```bash
   C:\Python311\python.exe -m pip install Django
   ```

### ❌ **Problem**: `Permission denied`
**What it means**: Need administrator privileges
**Solutions**:
1. **Run as Administrator**:
   - Right-click Command Prompt
   - Select "Run as administrator"

2. **Use user installation**:
   ```bash
   pip install --user Django
   ```

3. **Change directory permissions**:
   - Right-click project folder
   - Properties → Security → Edit permissions

### ❌ **Problem**: `setuptools.build_meta error`
**What it means**: Outdated setuptools
**Solutions**:
1. **Update setuptools**:
   ```bash
   python -m pip install --upgrade setuptools wheel
   ```

2. **Install pre-compiled packages**:
   ```bash
   pip install --only-binary=all Django
   ```

3. **Use conda instead**:
   ```bash
   conda install django
   ```

### ❌ **Problem**: `Microsoft Visual C++ required`
**What it means**: Need C++ compiler for building packages
**Solutions**:
1. **Install Visual Studio Build Tools**:
   - Download from Microsoft
   - Install C++ build tools

2. **Use pre-compiled packages**:
   ```bash
   pip install --only-binary=all -r requirements.txt
   ```

3. **Use conda** (includes pre-compiled packages)

---

## 🚀 Website Startup Problems

### ❌ **Problem**: `Port already in use`
**What it means**: Another program is using port 8000
**Solutions**:
1. **Use different port**:
   ```bash
   python manage.py runserver 8001
   ```

2. **Find what's using port 8000**:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Mac/Linux
   lsof -i :8000
   ```

3. **Kill the process**:
   ```bash
   # Windows (replace XXXX with PID)
   taskkill /PID XXXX /F
   ```

### ❌ **Problem**: `Module not found`
**What it means**: Package not installed
**Solutions**:
1. **Install missing package**:
   ```bash
   pip install package_name
   ```

2. **Check installed packages**:
   ```bash
   pip list
   ```

3. **Reinstall all packages**:
   ```bash
   pip install -r requirements.txt
   ```

### ❌ **Problem**: `Database connection error`
**What it means**: Database not accessible
**Solutions**:
1. **Check database file**:
   ```bash
   dir db.sqlite3
   ```

2. **Reset database**:
   ```bash
   python manage.py migrate --run-syncdb
   ```

3. **Create new database**:
   ```bash
   del db.sqlite3
   python manage.py migrate
   ```

### ❌ **Problem**: `Settings module not found`
**What it means**: Django can't find settings
**Solutions**:
1. **Check current directory**:
   ```bash
   dir manage.py
   ```

2. **Set Django settings**:
   ```bash
   set DJANGO_SETTINGS_MODULE=farmazee.settings
   ```

3. **Use full path**:
   ```bash
   python C:\path\to\farmazee\manage.py runserver
   ```

---

## 🗄️ Database Problems

### ❌ **Problem**: `No migrations to apply`
**What it means**: Database is up to date or no migrations exist
**Solutions**:
1. **Create migrations**:
   ```bash
   python manage.py makemigrations
   ```

2. **Force migration**:
   ```bash
   python manage.py migrate --run-syncdb
   ```

3. **Reset migrations**:
   ```bash
   python manage.py migrate --fake-initial
   ```

### ❌ **Problem**: `Table already exists`
**What it means**: Database tables conflict
**Solutions**:
1. **Fake initial migration**:
   ```bash
   python manage.py migrate --fake-initial
   ```

2. **Reset database**:
   ```bash
   del db.sqlite3
   python manage.py migrate
   ```

3. **Check migration history**:
   ```bash
   python manage.py showmigrations
   ```

### ❌ **Problem**: `Database is locked`
**What it means**: Another process is using database
**Solutions**:
1. **Close other Django processes**:
   - Press `Ctrl + C` in other Command Prompt windows
   - Close all Python processes

2. **Wait and retry**:
   - Wait 30 seconds
   - Try command again

3. **Restart computer** (last resort)

---

## 👑 Admin User Problems

### ❌ **Problem**: `No such command: create_admin_user`
**What it means**: Custom command not found
**Solutions**:
1. **Check if command exists**:
   ```bash
   python manage.py help
   ```

2. **Create superuser instead**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Check management commands**:
   ```bash
   dir core\management\commands\
   ```

### ❌ **Problem**: `Can't log into admin panel`
**What it means**: User doesn't exist or wrong credentials
**Solutions**:
1. **Create new superuser**:
   ```bash
   python manage.py createsuperuser
   ```

2. **Reset password**:
   ```bash
   python manage.py changepassword username
   ```

3. **Check user exists**:
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import User
   >>> User.objects.all()
   ```

### ❌ **Problem**: `Admin panel shows errors`
**What it means**: Template or view problems
**Solutions**:
1. **Check Django errors**:
   ```bash
   python manage.py check
   ```

2. **Check admin URLs**:
   ```bash
   python manage.py show_urls | findstr admin
   ```

3. **Restart server**:
   ```bash
   # Stop server (Ctrl + C)
   python manage.py runserver
   ```

---

## 🎨 Admin Panel Customization Problems

### ❌ **Problem**: `Changes not appearing on website`
**What it means**: Settings not saved or cache issue
**Solutions**:
1. **Check if settings saved**:
   - Go to admin panel
   - Check if changes are there

2. **Clear browser cache**:
   - Press `Ctrl + F5`
   - Or open in incognito mode

3. **Check database**:
   ```bash
   python manage.py shell
   >>> from core.models import SystemSettings
   >>> SystemSettings.objects.first()
   ```

### ❌ **Problem**: `Admin panel looks broken`
**What it means**: CSS/JavaScript not loading
**Solutions**:
1. **Check static files**:
   ```bash
   python manage.py collectstatic
   ```

2. **Check file permissions**:
   - Ensure static folder is readable

3. **Check browser console**:
   - Press `F12` in browser
   - Look for error messages

### ❌ **Problem**: `Feature toggles not working`
**What it means**: Settings not applied correctly
**Solutions**:
1. **Check feature settings**:
   - Go to System Settings → Feature Toggles
   - Ensure settings are saved

2. **Check template logic**:
   - Look for `{% if enable_feature %}` in templates

3. **Restart server**:
   - Stop and start server again

---

## 🌐 Browser Problems

### ❌ **Problem**: `Website shows blank page`
**What it means**: Server not running or error occurred
**Solutions**:
1. **Check server status**:
   - Look at Command Prompt
   - Should show "Starting development server"

2. **Check browser console**:
   - Press `F12`
   - Look for error messages

3. **Try different browser**:
   - Chrome, Firefox, Edge

### ❌ **Problem**: `CSS not loading`
**What it means**: Static files not accessible
**Solutions**:
1. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

2. **Check static folder**:
   ```bash
   dir static\
   ```

3. **Check settings.py**:
   - Ensure `STATIC_URL` and `STATICFILES_DIRS` are set

### ❌ **Problem**: `Images not showing`
**What it means**: Media files not accessible
**Solutions**:
1. **Check media folder**:
   ```bash
   dir media\
   ```

2. **Check file permissions**:
   - Ensure media folder is readable

3. **Check settings.py**:
   - Ensure `MEDIA_URL` and `MEDIA_ROOT` are set

---

## 🔍 Debugging Tools

### 📊 **Django Debug Toolbar**
```bash
pip install django-debug-toolbar
```
Add to `settings.py`:
```python
INSTALLED_APPS = [
    'debug_toolbar',
    # ... other apps
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... other middleware
]
```

### 📝 **Django Extensions**
```bash
pip install django-extensions
```
Add to `settings.py`:
```python
INSTALLED_APPS = [
    'django_extensions',
    # ... other apps
]
```

### 🔍 **Useful Commands**
```bash
# Check system health
python manage.py check

# Show all URLs
python manage.py show_urls

# Show migrations
python manage.py showmigrations

# Shell for debugging
python manage.py shell

# Validate models
python manage.py validate
```

---

## 🚨 Emergency Recovery

### 💾 **Backup Database**
```bash
# Copy database file
copy db.sqlite3 db_backup.sqlite3

# Or use Django dumpdata
python manage.py dumpdata > backup.json
```

### 🔄 **Reset Everything**
```bash
# Stop server
# Delete database
del db.sqlite3

# Delete migrations
del core\migrations\0*.py
del crops\migrations\0*.py
del weather\migrations\0*.py
del soil_health\migrations\0*.py
del marketplace\migrations\0*.py
del community\migrations\0*.py
del schemes\migrations\0*.py
del ai_chatbot\migrations\0*.py

# Recreate everything
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py init_system_settings
```

### 🆘 **Get Help**
1. **Check error messages** carefully
2. **Search online** for the error
3. **Ask in forums** (Stack Overflow, Django forums)
4. **Check Django documentation**
5. **Ask a programmer friend**

---

## 🎯 **Prevention Tips**

### ✅ **Before Starting**:
- Use virtual environment
- Check Python version compatibility
- Install packages one by one
- Keep backups of working versions

### ✅ **While Working**:
- Test changes in small steps
- Keep Command Prompt open
- Monitor error messages
- Save work frequently

### ✅ **After Changes**:
- Test website functionality
- Check admin panel
- Verify settings work
- Keep notes of what you changed

---

## 🏆 **Success Checklist**

### ✅ **Installation Complete**:
- [ ] Python installed and in PATH
- [ ] All packages installed
- [ ] No error messages

### ✅ **Website Working**:
- [ ] Server starts without errors
- [ ] Website opens in browser
- [ ] All pages load correctly

### ✅ **Admin Panel Working**:
- [ ] Can log in with admin account
- [ ] All menu options visible
- [ ] Can change settings
- [ ] Changes appear on website

### ✅ **Customization Working**:
- [ ] Can change colors
- [ ] Can change text
- [ ] Can toggle features
- [ ] Can update content

---

## 🎊 **You're Ready!**

With this troubleshooting guide, you can:
- 🔧 Fix common problems
- 🚨 Handle emergencies
- 🔍 Debug issues
- 🛡️ Prevent problems
- 🚀 Get back to building!

**Remember**: Every problem has a solution. Keep trying! 💪
