"""
Tests for player APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from goal_maven.core.models import Continent
# from goal_maven.core import models

from goal_maven.core.tests.helper_methods import HelperMethods

from goal_maven.continent.serializers import (
    ContinentSerializer,
    ContinentDetailSerializer,
)

# import pdb

# PLAYERS_URL = reverse('player:player-list')
CONTINENTS_URL = reverse('continent:continent-list')


def detail_url(continent_id):
    """Create and return a continent detail URL."""
    return reverse('continent:continent-detail', args=[continent_id])


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CONTINENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.staff_user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            first_name='test',
            last_name='user',
            is_staff=True,
        )
        self.client.force_authenticate(self.staff_user)
        self.helper = HelperMethods()

    def test_retrieve_continents(self):
        """Test retrieving a list of continents."""
        self.helper.create_continent(continent_name='continent1')
        self.helper.create_continent(continent_name='continent2')

        res = self.client.get(CONTINENTS_URL)

        continents = Continent.objects.all().order_by('continent_id')
        serializer = ContinentSerializer(continents, many=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_continent_detail(self):
        """Test get continent detail."""
        continent = self.helper.create_continent(continent_name='continent1')

        url = detail_url(continent.continent_id)
        res = self.client.get(url)

        serializer = ContinentDetailSerializer(continent)
        self.assertEqual(res.data, serializer.data)

    def test_create_continent(self):
        """Test creating a continent."""
        # nation = self.helper.create_nation(nation_name='Pakistan')
        # role = self.helper.create_playerrole(role_name='Striker')
        # team = self.helper.create_team(team_name='Askari Strikers')
        payload = {
            'continent_name': 'continent1',
        }
        # pdb.set_trace()
        res = self.client.post(CONTINENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        continent = Continent.objects.get(continent_id=res.data['continent_id'])
        for k, v in payload.items():
            self.assertEqual(getattr(continent, k), v)
        self.assertEqual(continent.continent_name, 'continent1')
