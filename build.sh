#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create categories for farmer problems if they don't exist
python manage.py create_problem_categories

# Create superuser if needed (optional - comment out if not needed)
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@farmazee.com', 'AdminPass123!')"

echo "Build completed successfully!"

# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create categories for farmer problems if they don't exist
python manage.py create_problem_categories

# Create superuser if needed (optional - comment out if not needed)
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@farmazee.com', 'AdminPass123!')"

echo "Build completed successfully!"

