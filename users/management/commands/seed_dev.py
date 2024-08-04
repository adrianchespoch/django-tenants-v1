from django.core.management.base import BaseCommand

from backend.shared.seeders.dev.users_seed import seed_users


class Command(BaseCommand):
    help = 'Seed development database with data'

    def handle(self, *args, **options):
        print('Seeding development database...')
        try:
            seed_users()
            self.stdout.write(self.style.SUCCESS(
                '[USERS]: Successfully seeded development database'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'[USERS]: Error seeding development database: {e}'))
