from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create a superuser for admin panel access'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--email', type=str, default='admin@farmazee.com', help='Admin email')
        parser.add_argument('--password', type=str, default='admin123', help='Admin password')
        parser.add_argument('--first-name', type=str, default='Admin', help='Admin first name')
        parser.add_argument('--last-name', type=str, default='User', help='Admin last name')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Skipping creation.')
            )
            return

        # Create superuser
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created superuser "{username}" with email "{email}"'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Password: {password}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'You can now access the admin panel at /admin-panel/dashboard/'
            )
        )
