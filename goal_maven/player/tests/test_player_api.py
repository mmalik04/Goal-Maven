"""
Tests for player APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from goal_maven.core.models import Player

from goal_maven.core.tests.helper_methods import HelperMethods

from goal_maven.player.serializers import (
    PlayerSerializer,
    PlayerDetailSerializer,
)

from datetime import datetime

# import pdb

PLAYERS_URL = reverse('player:player-list')


def detail_url(player_id):
    """Create and return a player detail URL."""
    return reverse('player:player-detail', args=[player_id])


class PublicPlayerAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PLAYERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlayerApiTests(TestCase):
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

    def test_retrieve_players(self):
        """Test retrieving a list of players."""
        self.helper.create_player(player_name='Player1')
        self.helper.create_player(player_name='Player2')

        res = self.client.get(PLAYERS_URL)

        players = Player.objects.all().order_by('player_id')
        serializer = PlayerSerializer(players, many=True)
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_player_detail(self):
        """Test get player detail."""
        player = self.helper.create_player(player_name='Player1')

        url = detail_url(player.player_id)
        res = self.client.get(url)

        serializer = PlayerDetailSerializer(player)
        self.assertEqual(res.data, serializer.data)

    def test_create_player(self):
        """Test creating a player."""
        nation = self.helper.create_nation(nation_name='Pakistan')
        role = self.helper.create_playerrole(role_name='Striker')
        team = self.helper.create_team(team_name='Askari Strikers')
        payload = {
            'player_name': 'Player1',
            'jersy_number': '7',
            'date_of_birth': datetime.strptime('1996-01-05', '%Y-%m-%d').date(),
            'career_start': datetime.strptime('2008-01-01', '%Y-%m-%d').date(),
            'nation': nation.nation_id,
            'team': team.team_id,
            'role': role.role_id,
            'height': 1.82,
            'weight': 85,
            'total_appearances': 50,
        }
        # pdb.set_trace()
        res = self.client.post(PLAYERS_URL, payload)
        player = Player.objects.get(player_id=res.data['player_id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Player.objects.filter(player_id=res.data['player_id']).exists(),
            True,
        )
        self.assertEqual(player.player_name, 'Player1')

    def test_partial_update(self):
        """Test partial update of a player."""
        team = self.helper.create_team(
            team_name='Saqlain FC'
        )
        player = self.helper.create_player(
            player_name='Bashir',
        )

        payload = {'team': team.team_id}
        url = detail_url(player.player_id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        player.refresh_from_db()
        self.assertEqual(player.team.team_id, payload['team'])

    def test_full_update(self):
        """Test full update of player."""
        player = self.helper.create_player(
            player_name='Lionel Messi',
        )
        nation = self.helper.create_nation(nation_name='Portugal')
        role = self.helper.create_playerrole(role_name='Striker')
        team = self.helper.create_team(team_name='Real Madrid')
        payload = {
            'player_name': 'Cristiano Ronaldo',
            'jersy_number': '7',
            'date_of_birth': datetime.strptime('1996-01-05', '%Y-%m-%d').date(),
            'career_start': datetime.strptime('2008-01-01', '%Y-%m-%d').date(),
            'nation': nation.nation_id,
            'team': team.team_id,
            'role': role.role_id,
            'height': 1.82,
            'weight': 85,
            'total_appearances': 500,
        }

        url = detail_url(player.player_id)
        res = self.client.put(url, payload)
        player.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(player.player_name, payload['player_name'])
        self.assertEqual(player.jersy_number, payload['jersy_number'])
        self.assertEqual(player.date_of_birth, payload['date_of_birth'])
        self.assertEqual(player.career_start, payload['career_start'])
        self.assertEqual(player.nation.nation_id, payload['nation'])
        self.assertEqual(player.team.team_id, payload['team'])
        self.assertEqual(player.role.role_id, payload['role'])
        self.assertEqual(player.height, payload['height'])
        self.assertEqual(player.weight, payload['weight'])
        self.assertEqual(player.total_appearances, payload['total_appearances'])

    # def test_update_user_returns_error(self):
    #     """Test changing the recipe user results in an error."""
    #     new_user = create_user(email='user2@example.com', password='test123')
    #     recipe = create_recipe(user=self.user)

    #     payload = {'user': new_user.id}
    #     url = detail_url(recipe.id)
    #     self.client.patch(url, payload)

    #     recipe.refresh_from_db()
    #     self.assertEqual(recipe.user, self.user)

    # def test_delete_recipe(self):
    #     """Test deleting a recipe successful."""
    #     recipe = create_recipe(user=self.user)

    #     url = detail_url(recipe.id)
    #     res = self.client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    # def test_recipe_other_users_recipe_error(self):
    #     """Test trying to delete another users recipe gives error."""
    #     new_user = create_user(email='user2@example.com', password='test123')
    #     recipe = create_recipe(user=new_user)

    #     url = detail_url(recipe.id)
    #     res = self.client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
