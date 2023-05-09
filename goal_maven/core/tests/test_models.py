"""
Tests for models.
"""
from datetime import datetime
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123',
                first_name='test',
                last_name='user',
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_new_user_with_correct_name_created(self):
        """Test user's first and last name is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_new_user_without_name_raises_error(self):
        """Test user's empty last name raises error."""
        email = 'test@example.com'
        password = 'testpass123'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
            )

    def test_new_user_with_correct_username_created(self):
        """Test user's username is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        username = 'testuser69'
        first_name = 'test'
        last_name = 'user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.username, username)

    def test_new_user_with_correct_dob_created(self):
        """Test user's dob is added correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        date_of_birth = datetime(1996, 1, 5).date()
        date_of_birth = date_of_birth.strftime('%Y-%m-%d')
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )

        self.assertEqual(user.date_of_birth, date_of_birth)

    def test_new_user_with_invalid_dob_raises_error(self):
        """Test user's invalid dob raises error."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        date_of_birth = datetime.now() + timedelta(days=1)
        date_of_birth = date_of_birth.date().strftime('%Y-%m-%d')
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
            )

    def test_new_user_with_lessthan5yr_dob_raises_error(self):
        """Test user's dob less than 5 year raises error."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        date_of_birth = datetime.now() - timedelta(days=1824)
        date_of_birth = date_of_birth.date().strftime('%Y-%m-%d')
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
            )

    def test_new_user_with_favourite_team_created(self):
        """Test user's favourite Team is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        favorite_team = 'Real Madrid'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            favorite_team=favorite_team,
        )

        self.assertEqual(user.favorite_team, favorite_team)

    def test_new_user_with_favourite_players_created(self):
        """Test user's username is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        favorite_players = 'Cristiano Ronaldo, Lionel Messi'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            favorite_players=favorite_players,
        )

        self.assertEqual(user.favorite_players, favorite_players)

    def test_new_user_with_country_created(self):
        """Test user's country is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        country = 'Pakistan'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            country=country,
        )

        self.assertEqual(user.country, country)

    def test_update_user_details_is_successful(self):
        """Test updating user's details is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'test'
        last_name = 'user'
        country = 'Pakistan'
        date_of_birth = '1997-01-05'
        favorite_team = 'Bayern Munich'
        favorite_players = 'Karim Benzema'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        updated_password = 'updatedtestpass123'
        updated_first_name = 'updated_test'
        updated_last_name = 'updated_user'
        extra_fields = {
            'first_name': updated_first_name,
            'last_name': updated_last_name,
            'country': country,
            'date_of_birth': date_of_birth,
            'favorite_team': favorite_team,
            'favorite_players': favorite_players,
        }

        updated_user = get_user_model().objects.update_user(
            user=user,
            password=updated_password,
            **extra_fields,
        )

        self.assertEqual(updated_user.email, email)
        self.assertEqual(updated_user.first_name, updated_first_name)
        self.assertEqual(updated_user.last_name, updated_last_name)
        self.assertEqual(updated_user.country, country)
        self.assertEqual(updated_user.date_of_birth, date_of_birth)
        self.assertEqual(updated_user.favorite_team, favorite_team)
        self.assertEqual(updated_user.favorite_players, favorite_players)
        self.assertTrue(updated_user.check_password(updated_password))

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
            first_name='test',
            last_name='superuser'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
