# """
# Django test command.
# """
# import os

# from django.core.management.base import BaseCommand


# class Command(BaseCommand):
#     """Django command to test anything."""

#     def handle(self, *args, **options):
#         """Entrypoint for command."""
#         self.stdout.write(self.style.SUCCESS(os.getcwd()))

#         self.stdout.write('Waiting for database...')
#         db_up = False
#         while db_up is False:
#             try:
#                 self.check(databases=['default'])
#                 db_up = True
#             except (Psycopg2OpError, OperationalError):
#                 self.stdout.write('Database unavailable, waiting 1 second...')
#                 time.sleep(1)

#         self.stdout.write(self.style.SUCCESS('Database available!'))
