# 🚀 Farmazee - Step by Step Guide

## 📋 What You'll Need Before Starting

### 🖥️ Your Computer
- Windows, Mac, or Linux computer
- Internet connection
- Web browser (Chrome, Firefox, Edge)

### 🐍 Python (The Magic Language)
- **Download**: Go to [python.org](https://python.org)
- **Install**: Run the installer
- **Important**: ✅ Check "Add Python to PATH"

### 📁 Project Files
- Download Farmazee project
- Extract to a folder (like `C:\farmazee`)

---

## 🎯 STEP 1: Open the Magic Door (Command Prompt)

### Windows:
1. Press `Windows + R` keys
2. Type `cmd` and press Enter
3. You'll see a black window - that's your magic door! 🚪

### Mac/Linux:
1. Press `Command + Space`
2. Type `terminal` and press Enter
3. You'll see a white/black window

---

## 🔧 STEP 2: Go to Your Project Folder

### In the Command Prompt, type:
```bash
cd C:\farmazee
```
**What this means**: "Go to the farmazee folder"

### Press Enter! ✅

**You should see**: `C:\farmazee>` at the start of the line

---

## 📦 STEP 3: Install the Magic Tools

### Install each tool one by one:

```bash
pip install Django
```
**Wait for it to finish, then:**
```bash
pip install djangorestframework
```
**Wait for it to finish, then:**
```bash
pip install django-cors-headers
```
**Wait for it to finish, then:**
```bash
pip install django-crispy-forms
```
**Wait for it to finish, then:**
```bash
pip install crispy-bootstrap5
```
**Wait for it to finish, then:**
```bash
pip install Pillow
```

**What you're doing**: Installing the building blocks for your website! 🧱

---

## 🗄️ STEP 4: Create the Database

### Type these commands one by one:

```bash
python manage.py makemigrations
```
**Wait for it to finish, then:**
```bash
python manage.py migrate
```

**What this does**: Creates a place to store all the information (like creating a filing cabinet!) 📁

---

## 👑 STEP 5: Create Your Admin Account

### Type this command:
```bash
python manage.py create_admin_user
```

**What happens**:
1. It asks for a username (like your game character name!)
2. It asks for an email (your email address)
3. It asks for a password (make it strong!)
4. It asks you to type the password again

**Example**:
```
Username: farmer123
Email: farmer@example.com
Password: MyStrongPassword123!
```

---

## 🚀 STEP 6: Start Your Website!

### Type this command:
```bash
python manage.py runserver
```

**What happens**:
- You'll see lots of text
- Look for: `Starting development server at http://127.0.0.1:8000/`
- **Don't close this window!** Keep it open

---

## 🌐 STEP 7: Open Your Website!

### In your web browser:
1. Open a new tab
2. Type: `http://localhost:8000`
3. Press Enter

**🎉 Congratulations! You should see your Farmazee website!**

---

## 🎛️ STEP 8: Access the Control Room (Admin Panel)

### In your browser:
1. Go to: `http://localhost:8000/admin-panel/`
2. Log in with your username and password
3. **Welcome to the Control Room!** 🎮

---

## 🎨 STEP 9: Customize Your Website!

### In the Admin Panel, you can:

#### 🌈 **Change Colors** (Like Painting!)
- Click "UI/UX Customization"
- Change Primary Color (main color)
- Change Secondary Color (second color)
- Change Accent Color (highlight color)

#### 📝 **Change Words** (Like Writing!)
- Click "Content Customization"
- Change Site Name (from "Farmazee" to anything you want!)
- Change Homepage Title
- Change Footer Text

#### 🚪 **Open/Close Features** (Like Light Switches!)
- Click "Feature Toggles"
- Turn Marketplace On/Off
- Turn Community On/Off
- Turn AI Chatbot On/Off

#### 🔍 **SEO Settings** (Like Making Your Website Famous!)
- Click "SEO Settings"
- Add Google Analytics ID
- Add Facebook Pixel ID
- Change Meta Description

---

## 🚨 What to Do If Something Goes Wrong

### ❌ **Problem**: "pip is not recognized"
**Solution**: Python is not installed or not in PATH
1. Reinstall Python
2. Make sure to check "Add to PATH"

### ❌ **Problem**: "Permission denied"
**Solution**: Run Command Prompt as Administrator
1. Right-click on Command Prompt
2. Select "Run as administrator"

### ❌ **Problem**: "Package not found"
**Solution**: Try updating pip first
```bash
python -m pip install --upgrade pip
```

### ❌ **Problem**: Website won't start
**Solution**: Check if port 8000 is free
```bash
python manage.py runserver 8001
```
Then go to: `http://localhost:8001`

---

## 🎯 **Quick Commands Reference**

### 🚀 **Start Website**:
```bash
python manage.py runserver
```

### 🛑 **Stop Website**:
Press `Ctrl + C` in the Command Prompt

### 🔄 **Restart Website**:
```bash
python manage.py runserver
```

### 📁 **Check Files**:
```bash
dir
```

### 🗄️ **Reset Database**:
```bash
python manage.py migrate --run-syncdb
```

---

## 🏆 **You Did It!**

### 🎉 **What You've Built**:
- ✅ A working website
- ✅ An admin control panel
- ✅ A database to store information
- ✅ The ability to customize everything

### 🌟 **What You've Learned**:
- How to use Command Prompt
- How to install Python packages
- How to start a Django website
- How to customize a website
- Basic web development concepts

### 🚀 **What You Can Do Next**:
- Add more features
- Change the design
- Add new pages
- Learn more about Django
- Build other websites

---

## 🆘 **Need Help?**

### 📚 **Read These**:
- `README_SIMPLE.md` - Simple explanation
- `INSTALLATION_GUIDE.md` - Technical help
- `README.md` - Full documentation

### 🆘 **Ask For Help**:
- Ask a parent or teacher
- Ask a programmer friend
- Search online for Django tutorials
- Join programming communities

---

## 📚 **Want to Learn More?**

### 🎨 **Visual Learning:**
- **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - See diagrams and flowcharts
- **[README_SIMPLE.md](README_SIMPLE.md)** - Super simple explanation

### 🔧 **Technical Help:**
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Installation troubleshooting
- **[TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)** - Fix any problem

### 📖 **Complete Documentation:**
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Guide to all documentation
- **[README.md](README.md)** - Full technical documentation

---

**🎊 Congratulations! You're now a website builder! 🎊**

*Remember: Every expert was once a beginner. Keep learning and building!* 🌟
