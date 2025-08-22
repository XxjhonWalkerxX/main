"""
Django management command to run custom registration migrations
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run migrations for custom registration fields'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Running custom registration migrations...')
        )
        
        try:
            # Make migrations for the custom registration app
            call_command('makemigrations', 'customregistration', verbosity=1)
            
            # Apply the migrations
            call_command('migrate', 'customregistration', verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully completed custom registration migrations!'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error running migrations: {str(e)}')
            )
