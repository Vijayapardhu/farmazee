"""
Management command to fix empty slugs in FarmerProblem instances
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from django.db import models
from farmer_problems.models import FarmerProblem


class Command(BaseCommand):
    help = 'Fix empty slugs in FarmerProblem instances'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find problems with empty or None slugs
        problems_with_empty_slugs = FarmerProblem.objects.filter(
            models.Q(slug__isnull=True) | models.Q(slug='')
        )
        
        count = problems_with_empty_slugs.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No problems with empty slugs found.')
            )
            return
        
        self.stdout.write(f'Found {count} problems with empty slugs.')
        
        if dry_run:
            self.stdout.write('DRY RUN - No changes will be made.')
        
        fixed_count = 0
        
        for problem in problems_with_empty_slugs:
            # Generate a unique slug
            base_slug = slugify(problem.title)
            if not base_slug:
                base_slug = 'problem'
            
            # Ensure uniqueness
            slug = base_slug
            counter = 1
            while FarmerProblem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            if dry_run:
                self.stdout.write(f'Would fix: "{problem.title}" -> slug: "{slug}"')
            else:
                problem.slug = slug
                problem.save(update_fields=['slug'])
                self.stdout.write(f'Fixed: "{problem.title}" -> slug: "{slug}"')
            
            fixed_count += 1
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully fixed {fixed_count} problem slugs.')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Would fix {fixed_count} problem slugs.')
            )


