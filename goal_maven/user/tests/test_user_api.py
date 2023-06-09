"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from datetime import date

from goal_maven.core.tests.helper_methods import HelperMethods


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()
        self.helper = HelperMethods()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        self.helper = HelperMethods()
        country = self.helper.create_nation(
            nation_name='TestNation',
        )
        team = self.helper.create_team(
            team_name='Real Madrid',
        )
        player = self.helper.create_player(
            player_name='Vinicius Jr.'
        )
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'user',
            'username': 'testuser123',
            'date_of_birth': date(1996, 1, 5),
            'country': country.nation_id,
            'favorite_team': [team.team_name],
            'favorite_players': [player.player_name],
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'username': 'newuser123'
        }
        self.helper.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'first_name': 'Test',
            'last_name': 'user',
            'username': 'user766',
            'date_of_birth': date(1996, 1, 5),
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user_success(self):
        """Test generates token for valid credentials."""
        email = 'thegreatuser@example.com'
        user_details = {
            'first_name': 'test',
            'last_name': 'user',
            'password': 'test-user-password123',
            'username': 'noobmaster88',
            'date_of_birth': date(1996, 1, 5)
        }

        create_user(email=email, **user_details)
        payload = {
            'email': email,
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials_error(self):
        """Test returns error if credentials invalid."""
        create_user(
            email='test@example.com',
            password='goodpass',
            first_name='test',
            last_name='user',
            username='noobmaster88',
            date_of_birth=date(1996, 1, 5),
        )

        payload = {
            'email': 'test@example.com',
            'password': 'badpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found_error(self):
        """Test error returned if user not found for given email."""
        payload = {
            'email': 'test@example.com',
            'password': 'pass123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password_error(self):
        """Test posting a blank password returns an error."""
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.helper = HelperMethods()
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            first_name='test',
            last_name='user',
            username='testuser123',
            date_of_birth=date(1996, 1, 5),
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'date_of_birth': self.user.date_of_birth.strftime('%Y-%m-%d'),
            'country': self.user.country,
            'favorite_team': self.user.favorite_team,
            'favorite_players': self.user.favorite_players,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_success(self):
        """Test updating the user profile for the authenticated user."""
        country = self.helper.create_nation(nation_name='Pakistan')
        favorite_team = self.helper.create_team(team_name='Arsenal')
        messi = self.helper.create_player(player_name='Messi')
        ronaldo = self.helper.create_player(player_name='Ronaldo')
        payload = {
            'email': self.user.email,
            'password': 'newpassword123',
            'first_name': 'updatedtest',
            'last_name': 'updateduser',
            'username': self.user.username,
            'date_of_birth': self.user.date_of_birth,
            'country': country.nation_id,
            'favorite_team': [favorite_team.team_name],
            'favorite_players': [messi.player_name, ronaldo.player_name],
        }

        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertEqual(self.user.country.nation_id, payload['country'])
        self.assertEqual(self.user.favorite_team, payload['favorite_team'])
        self.assertEqual(self.user.favorite_players, payload['favorite_players'])
        self.assertTrue(self.user.check_password(payload['password']))
