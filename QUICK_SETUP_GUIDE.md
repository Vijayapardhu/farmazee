# Quick Setup Guide - Farmazee Farmer Problems

## 🚀 Quick Start (5 Minutes)

### 1. Get Supabase Anon Key
```
1. Go to: https://supabase.com/dashboard
2. Select your project: hhixytzsroxmmmlknuck
3. Settings → API → Copy "anon public" key
4. Add to .env file:
   SUPABASE_KEY=your-key-here
```

### 2. Create Storage Bucket
```
1. Supabase Dashboard → Storage
2. New Bucket → Name: "farmer-images"
3. Public bucket: YES
4. Save
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Categories (Copy-Paste to Django Shell)
```bash
python manage.py shell
```

```python
from farmer_problems.models import ProblemCategory

categories = [
    ('Crop Diseases', 'crop-diseases', 'fas fa-virus', '#dc3545'),
    ('Pest Control', 'pest-control', 'fas fa-bug', '#ffc107'),
    ('Soil Health', 'soil-health', 'fas fa-mountain', '#795548'),
    ('Irrigation', 'irrigation', 'fas fa-tint', '#0dcaf0'),
    ('Fertilizers', 'fertilizers', 'fas fa-flask', '#28a745'),
    ('Weather Issues', 'weather-issues', 'fas fa-cloud', '#6c757d'),
    ('Equipment', 'equipment', 'fas fa-tools', '#fd7e14'),
    ('Market & Pricing', 'market-pricing', 'fas fa-chart-line', '#20c997'),
]

for name, slug, icon, color in categories:
    ProblemCategory.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'icon': icon, 'color': color, 'description': f'{name} related problems'}
    )

print("Categories created!")
exit()
```

### 5. Start Server
```bash
python manage.py runserver
```

### 6. Test It!
1. Visit: http://localhost:8000/problems/
2. Click "Ask Question"
3. Fill form & upload images
4. Submit!

## 📱 URLs

- **Problems List:** `/problems/`
- **Ask Question:** `/problems/create/`
- **Become Expert:** `/problems/become-expert/`
- **Categories:** `/problems/categories/`
- **Experts:** `/problems/experts/`

## 👤 Create Your First Expert

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from farmer_problems.models import ExpertProfile

# Get or create a user
user = User.objects.first()  # Or create one

# Create expert profile
expert = ExpertProfile.objects.create(
    user=user,
    expert_type='agronomist',
    qualification='PhD in Agriculture',
    institution='State Agricultural University',
    years_of_experience=10,
    specialization='Crop diseases and pest management',
    bio='Agricultural expert with 10 years experience',
    is_verified=True  # Auto-verify for testing
)

print(f"Expert created: {expert}")
exit()
```

## 🎯 Features Checklist

- [x] Active navigation highlighting
- [x] Supabase PostgreSQL database
- [x] Supabase image storage
- [x] Post problems with images
- [x] Expert solutions
- [x] Voting system
- [x] Solution acceptance
- [x] Expert verification
- [x] Reputation scoring
- [x] Comments
- [x] Categories & tags
- [x] Search & filters

## 🔑 Environment Variables

Make sure `.env` has:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=ApenXXFgk6RGYcQc
DB_HOST=db.hhixytzsroxmmmlknuck.supabase.co
DB_PORT=5432

SUPABASE_URL=https://hhixytzsroxmmmlknuck.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_STORAGE_BUCKET=farmer-images

GEMINI_API_KEY=AIzaSyDFCmoQCjp6qbUp_rDErGCgFQoBsJblMVQ
```

## 🆘 Common Issues

**Can't connect to database:**
```
Check internet connection
Verify Supabase project is active
Test: ping db.hhixytzsroxmmmlknuck.supabase.co
```

**Images not uploading:**
```
1. Check SUPABASE_KEY is set
2. Verify bucket "farmer-images" exists
3. Ensure bucket is public
```

**Static files missing:**
```bash
python manage.py collectstatic --noinput
```

## ✅ You're All Set!

The system is ready! Just need to:
1. Add Supabase anon key
2. Run migrations
3. Create categories
4. Start posting problems!

Visit: `http://localhost:8000/problems/`

Enjoy your Reddit-style farmer Q&A platform! 🌾

