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
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
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
            user = get_user_model().objects.create_user(email, 'sample123')
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

    def test_new_user_with_correct_username_created(self):
        """Test user's username is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        username = 'testuser69'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
        )

        self.assertEqual(user.username, username)

    def test_new_user_with_correct_dob_created(self):
        """Test user's dob is added correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        date_of_birth = datetime(1996, 1, 5).date()
        date_of_birth = date_of_birth.strftime('%Y-%m-%d')
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            date_of_birth=date_of_birth,
        )

        self.assertEqual(user.date_of_birth, date_of_birth)

    def test_new_user_with_invalid_dob_raises_error(self):
        """Test user's invalid dob raises error."""
        email = 'test@example.com'
        password = 'testpass123'
        date_of_birth = datetime.now() + timedelta(days=1)
        date_of_birth = date_of_birth.date().strftime('%Y-%m-%d')
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                date_of_birth=date_of_birth,
            )

    def test_new_user_with_lessthan5yr_dob_raises_error(self):
        """Test user's dob less than 5 year raises error."""
        email = 'test@example.com'
        password = 'testpass123'
        date_of_birth = datetime.now() - timedelta(days=1824)
        date_of_birth = date_of_birth.date().strftime('%Y-%m-%d')
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                date_of_birth=date_of_birth,
            )

    def test_new_user_with_favourite_team_created(self):
        """Test user's username is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        favorite_team = 'Real Madrid'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            favorite_team=favorite_team,
        )

        self.assertEqual(user.favorite_team, favorite_team)

    def test_new_user_with_favourite_players_created(self):
        """Test user's username is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        favorite_players = 'Cristiano Ronaldo, Lionel Messi'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            favorite_players=favorite_players,
        )

        self.assertEqual(user.favorite_players, favorite_players)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
