"""
Customized createsuperuser command.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import getpass
from datetime import datetime


class Command(BaseCommand):
    """Command to create super user."""
    help = 'Create a superuser with an email address instead of a username.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def handle(self, *args, **options):
        # Prompt for the email address
        email = None
        while not email:
            email = input('Email address: ')
            if not email:
                self.stderr.write('Error: Email address cannot be blank.')

        # Prompt for the password
        password = None
        while not password:
            password = getpass.getpass()
            password2 = getpass.getpass('Password (again): ')
            if password != password2:
                self.stderr.write("Error: Your passwords didn't match.")
                password = None
                continue

        # Prompt for the first name
        first_name_inp = None
        while not first_name_inp:
            first_name = 'Test'
            first_name_inp = input(f'First Name ({first_name}): ')
            if not first_name_inp:
                first_name_inp = first_name
                # self.stderr.write('Error: First Name cannot be blank.')

        # Prompt for the last name
        last_name_inp = None
        while not last_name_inp:
            last_name = 'Admin'
            last_name_inp = input(f'Last Name ({last_name}): ')
            if not last_name_inp:
                last_name_inp = last_name
                # self.stderr.write('Error: Last Name cannot be blank.')

        # Prompt for username
        username = None
        while not username:
            username = input('Username: ')
            if not username:
                self.stderr.write('Error: Username cannot be blank.')

        # Prompt for date of birth
        date_of_birth_inp = None
        while not date_of_birth_inp:
            date_of_birth = '1996-01-05'
            date_of_birth_inp = input(f'Date of birth ({date_of_birth}): ')
            if not date_of_birth_inp:
                date_of_birth_inp = date_of_birth
                # self.stderr.write('Error: Date of birth cannot be blank.')
        date_of_birth_format = datetime.strptime(date_of_birth_inp, '%Y-%m-%d').date()

        User = get_user_model()

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            User.objects.create_superuser(
                email=email,
                password=password,
                username=username,
                first_name=first_name_inp,
                last_name=last_name_inp,
                date_of_birth=date_of_birth_format,
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stderr.write('A user with that email address already exists.')
