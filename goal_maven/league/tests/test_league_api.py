"""
Tests for League APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from goal_maven.core.models import League, LeagueTable
from goal_maven.core import models

from goal_maven.core.tests.helper_methods import HelperMethods

from goal_maven.league.serializers import (
    LeagueSerializer,
    LeagueDetailSerializer,
    LeagueTableSerializer,
    LeagueTableDetailSerializer,
)

# from django.core.management import call_command
# import pdb


def leagues_url(season_name):
    """Create and return a league list URL."""
    return reverse('league:league-list', args=[season_name])


def league_tables_url(season_name):
    """Create and return a league table list URL."""
    return reverse('league:league-table-list', args=[season_name])


def detail_url_league(league_id):
    """Create and return a league detail URL."""
    return reverse('league:league-detail', args=[league_id])


def detail_url_league_table(table_id):
    """Create and return a league table detail URL."""
    return reverse('league:league-table-detail', args=[table_id])


class PublicLeagueAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.helper = HelperMethods()

    def test_auth_required(self):
        """Test auth is required to call API."""
        season = self.helper.create_season(season_name='testseason1')
        res = self.client.get(leagues_url(season.season_name))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLeagueApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.staff_client = APIClient()
        self.normal_client = APIClient()
        self.helper = HelperMethods()
        self.staff_user = self.helper.get_staff()
        self.normal_user = self.helper.get_user()
        self.staff_client.force_authenticate(self.staff_user)
        self.normal_client.force_authenticate(self.normal_user)

    def test_retrieve_leagues(self):
        """Test retrieving a list of leagues."""
        season = self.helper.create_season(season_name='season1')
        self.helper.create_league(league_name='league1', season=season)
        self.helper.create_league(league_name='league2', season=season)

        res = self.normal_client.get(leagues_url(season.season_name))

        leagues = League.objects.filter(season=season)
        serializer = LeagueSerializer(leagues, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_league_tables(self):
        """Test retrieving a list of league tables of leagues."""
        season = self.helper.create_season(season_name='testseason')
        league1 = self.helper.create_league(league_name='league1', season=season)
        team1 = self.helper.create_team(team_name='team1')
        self.helper.create_leaguetable(
            team=team1, league=league1, season=season, position=1,
        )
        league2 = self.helper.create_league(league_name='league2', season=season)
        team2 = self.helper.create_team(team_name='team2')
        self.helper.create_leaguetable(
            team=team2, league=league2, season=season, position=1,
        )
        league3 = self.helper.create_league(league_name='league3', season=season)
        team3 = self.helper.create_team(team_name='team13')
        self.helper.create_leaguetable(
            team=team3, league=league3, season=season, position=1,
        )

        res = self.normal_client.get(league_tables_url(season.season_name))

        league_tables = models.LeagueTable.objects.filter(season=season)

        serializer = LeagueTableSerializer(league_tables, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_league_detail(self):
        """Test get league detail."""
        season = self.helper.create_season(season_name='season3')
        league = self.helper.create_league(league_name='league3', season=season)

        res = self.normal_client.get(detail_url_league(league.league_id))

        serializer = LeagueDetailSerializer(league)
        self.assertEqual(res.data, serializer.data)

    def test_get_league_tables(self):
        """Test get league table detail."""
        season = self.helper.create_season(season_name='testseason')
        league1 = self.helper.create_league(league_name='league1', season=season)
        team = self.helper.create_team(team_name='team1')
        table_team1 = self.helper.create_leaguetable(
            team=team, league=league1, season=season, position=1,
        )

        res = self.normal_client.get(detail_url_league_table(table_team1.table_id))

        serializer = LeagueTableDetailSerializer(table_team1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_league(self):
        """Test creating a league."""
        nation = self.helper.create_nation(nation_name='testnation')
        season = self.helper.create_season(season_name='testseason')
        player = self.helper.create_player(player_name='testplayer')
        payload = {
            'league_name': 'test league',
            'nation': nation.nation_id,
            'season': season.season_id,
            'top_scorer': player.player_id,
        }
        res = self.staff_client.post(leagues_url(season.season_name), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        league = League.objects.get(league_id=res.data['league_id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(League.objects.filter(league_id=res.data['league_id']).exists())
        self.assertEqual(league.league_name, 'test league')

    def test_create_league_table(self):
        """Test creating a league table."""
        league = self.helper.create_league(league_name='test league')
        season = self.helper.create_season(season_name='this season')
        team = self.helper.create_team(team_name='test player')
        payload = {
            'league': league.league_id,
            'season': season.season_id,
            'team': team.team_id,
        }

        res = self.staff_client.post(league_tables_url(season.season_name), payload)
        league_table_obj = models.LeagueTable.objects.get(table_id=res.data['table_id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(league_table_obj.league.league_id, league.league_id)
        self.assertEqual(league_table_obj.season.season_id, season.season_id)
        self.assertEqual(league_table_obj.team.team_id, team.team_id)

    def test_create_league_by_normaluser_returns_error(self):
        """Test creating a league with normal user returns error."""
        nation = self.helper.create_nation(nation_name='testnation')
        season = self.helper.create_season(season_name='testseason')
        player = self.helper.create_player(player_name='testplayer')
        payload = {
            'league_name': 'test league',
            'nation': nation.nation_id,
            'season': season.season_id,
            'top_scorer': player.player_id,
        }

        res = self.normal_client.post(leagues_url(season.season_name), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_league_table_by_normaluser_returns_error(self):
        """Test creating a league table with normal user returns error."""
        league = self.helper.create_league(league_name='test league')
        season = self.helper.create_season(season_name='this season')
        team = self.helper.create_team(team_name=' test team')
        self.helper.create_leaguetable(team=team)
        payload = {
            'league': league.league_id,
            'season': season.season_id,
            'team': team.team_id,
        }

        res = self.normal_client.post(league_tables_url(season.season_name), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_league(self):
        """Test partial update of a league."""
        player = self.helper.create_player(player_name='test player')
        season = self.helper.create_season(season_name='test season')
        league = self.helper.create_league(season=season)

        payload = {'top_scorer': player.player_id}
        url = detail_url_league(league.league_id)
        res = self.staff_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        league.refresh_from_db()
        self.assertEqual(league.top_scorer.player_id, payload['top_scorer'])

    def test_partial_league_table(self):
        """Test partial update of a league table."""
        league = self.helper.create_league(league_name='test league')
        season = self.helper.create_season(season_name='this season')
        team = self.helper.create_team(team_name='test player')
        table_entry = self.helper.create_leaguetable(
            league=league,
            season=season,
            team=team,
            position=2
        )
        payload = {
            'points': 70,
            'position': 1,
        }

        url = detail_url_league_table(table_entry.table_id)
        res = self.staff_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        table_entry.refresh_from_db()
        self.assertEqual(table_entry.position, payload['position'])
        self.assertEqual(table_entry.points, payload['points'])

    def test_partial_update_leauge_by_normaluser_returns_error(self):
        """Test partial update league with normal user returns error."""
        player = self.helper.create_player(player_name='test player')
        season = self.helper.create_season(season_name='test season')
        league = self.helper.create_league(season=season)

        payload = {'top_scorer': player.player_id}
        url = detail_url_league(league.league_id)

        res = self.normal_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_leauge_table_by_normaluser_returns_error(self):
        """Test partial update league table with normal user returns error."""
        league = self.helper.create_league(league_name='test league')
        season = self.helper.create_season(season_name='this season')
        team = self.helper.create_team(team_name='test player')
        table_entry = self.helper.create_leaguetable(
            league=league,
            season=season,
            team=team,
            position=2
        )
        payload = {
            'points': 70,
            'position': 1,
        }

        url = detail_url_league_table(table_entry.table_id)

        res = self.normal_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_league(self):
        """Test full update of league."""
        league = self.helper.create_league('test league')

        nation = self.helper.create_nation(nation_name='testnation')
        season = self.helper.create_season(season_name='testseason')
        player = self.helper.create_player(player_name='testplayer')
        payload = {
            'league_name': 'test league',
            'nation': nation.nation_id,
            'season': season.season_id,
            'top_scorer': player.player_id,
        }

        url = detail_url_league(league.league_id)
        res = self.staff_client.put(url, payload)
        league.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(league.league_name, payload['league_name'])
        self.assertEqual(league.nation.nation_id, payload['nation'])
        self.assertEqual(league.season.season_id, payload['season'])
        self.assertEqual(league.top_scorer.player_id, payload['top_scorer'])

    def test_full_update_league_table(self):
        """Test full update of league table."""
        team = self.helper.create_team(team_name='test team')
        table_entry = self.helper.create_leaguetable(team=team)

        league = self.helper.create_league(league_name='test league')
        season = self.helper.create_season(season_name='this season')
        payload = {
            'league': league.league_id,
            'season': season.season_id,
            'team': team.team_id,
        }

        url = detail_url_league_table(table_entry.table_id)

        res = self.staff_client.put(url, payload)
        table_entry.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(table_entry.league.league_id, league.league_id)
        self.assertEqual(table_entry.season.season_id, season.season_id)
        self.assertEqual(table_entry.team.team_id, team.team_id)

    def test_full_update_league_by_normaluser_returns_error(self):
        """Test full update of league with normal user returns error."""
        league = self.helper.create_league('test league')

        nation = self.helper.create_nation(nation_name='testnation')
        season = self.helper.create_season(season_name='testseason')
        player = self.helper.create_player(player_name='testplayer')
        payload = {
            'league_name': 'test league',
            'nation': nation.nation_id,
            'season': season.season_id,
            'top_scorer': player.player_id,
        }

        url = detail_url_league(league.league_id)
        res = self.normal_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(league.league_name, 'test league')

    def test_full_update_league_table_by_normaluser_returns_error(self):
        """Test full update of league table with normal user returns error."""
        team = self.helper.create_team(team_name='test team')
        league = self.helper.create_league(league_name='test league')
        table_entry = self.helper.create_leaguetable(team=team, league=league)

        league = self.helper.create_league(league_name='new league')
        season = self.helper.create_season(season_name='this season')
        payload = {
            'league': league.league_id,
            'season': season.season_id,
            'team': team.team_id,
        }

        url = detail_url_league_table(table_entry.table_id)
        res = self.normal_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(table_entry.league.league_name, 'test league')

    def test_delete_league(self):
        """Test deleting a league successful."""
        league = self.helper.create_league(league_name='test league')

        url = detail_url_league(league.league_id)
        res = self.staff_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(League.objects.filter(league_id=league.league_id).exists())

    def test_delete_league_table(self):
        """Test deleting a league table successful."""
        team = self.helper.create_team(team_name='test team')
        league = self.helper.create_league(league_name='test league')
        table_entry = self.helper.create_leaguetable(team=team, league=league)

        url = detail_url_league_table(table_entry.table_id)
        res = self.staff_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            LeagueTable.objects.filter(table_id=table_entry.table_id).exists()
        )

    def test_delete_league_by_normaluser_returns_error(self):
        """Test deleting a league with normal user returns error."""
        league = self.helper.create_league(league_name='test league')

        url = detail_url_league(league.league_id)
        res = self.normal_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(League.objects.filter(league_id=league.league_id).exists())

    def test_delete_league_table_by_normaluser_returns_error(self):
        """Test deleting a league table with normal user returns error."""
        team = self.helper.create_team(team_name='test team')
        league = self.helper.create_league(league_name='test league')
        table_entry = self.helper.create_leaguetable(team=team, league=league)

        url = detail_url_league_table(table_entry.table_id)
        res = self.normal_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            LeagueTable.objects.filter(table_id=table_entry.table_id).exists()
        )
