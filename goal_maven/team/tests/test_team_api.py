"""
Tests for Team APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from goal_maven.core.models import Team
from goal_maven.core import models

from goal_maven.core.tests.helper_methods import HelperMethods

from goal_maven.team.serializers import (
    TeamSerializer,
    TeamDetailSerializer,
    TeamStatsSerializer,
)

# from django.core.management import call_command

from datetime import datetime


TEAMS_URL = reverse('team:team-list')


def detail_url(team_id):
    """Create and return a team detail URL."""
    return reverse('team:team-detail', args=[team_id])


def stats_url(team_id, season_name):
    """Create and return a team stats URL."""
    return reverse('team:team-season-stats', args=[team_id, season_name])


class PublicTeamAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TEAMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTeamApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.staff_client = APIClient()
        self.normal_client = APIClient()
        self.helper = HelperMethods()
        self.staff_user = self.helper.get_staff()
        self.normal_user = self.helper.get_user()
        self.staff_client.force_authenticate(self.staff_user)
        self.normal_client.force_authenticate(self.normal_user)

    def test_retrieve_teams(self):
        """Test retrieving a list of teams."""
        self.helper.create_team(team_name='team1')
        self.helper.create_team(team_name='team2')

        res = self.normal_client.get(TEAMS_URL)

        teams = Team.objects.all().order_by('team_id')
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_team_detail(self):
        """Test get team detail."""
        team = self.helper.create_team(team_name='team3')

        res = self.normal_client.get(detail_url(team.team_id))

        serializer = TeamDetailSerializer(team)
        self.assertEqual(res.data, serializer.data)

    def test_create_team(self):
        """Test creating a team."""
        league = self.helper.create_league(league_name='testleague')
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        manager = self.helper.create_manager(manager_name='testmanager')
        payload = {
            'team_name': 'team1',
            'est_date': datetime.strptime('1900-01-05', '%Y-%m-%d').date(),
            'league': league.league_id,
            'stadium': stadium.stadium_id,
            'manager': manager.manager_id,
        }
        res = self.staff_client.post(TEAMS_URL, payload)
        team = Team.objects.get(team_id=res.data['team_id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(team_id=res.data['team_id']).exists())
        self.assertEqual(team.team_name, 'team1')

    def test_create_team_by_normaluser_returns_error(self):
        """Test creating a team with normal user returns error."""
        league = self.helper.create_league(league_name='testleague')
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        manager = self.helper.create_manager(manager_name='testmanager')
        payload = {
            'team_name': 'team1',
            'est_date': datetime.strptime('1900-01-05', '%Y-%m-%d').date(),
            'league': league.league_id,
            'stadium': stadium.stadium_id,
            'manager': manager.manager_id,
        }
        res = self.normal_client.post(TEAMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update(self):
        """Test partial update of a team."""
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        team = self.helper.create_team(
            team_name='Bashir FC',
        )

        payload = {'stadium': stadium.stadium_id}
        url = detail_url(team.team_id)
        res = self.staff_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        team.refresh_from_db()
        self.assertEqual(team.stadium.stadium_id, payload['stadium'])

    def test_partial_update_by_normaluser_returns_error(self):
        """Test partial update with normal user returns error."""
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        team = self.helper.create_team(
            team_name='Bashir FC',
        )

        payload = {'stadium': stadium.stadium_id}
        url = detail_url(team.team_id)
        res = self.normal_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update(self):
        """Test full update of team."""
        team = self.helper.create_team(
            team_name='My Team',
        )
        league = self.helper.create_league(league_name='testleague')
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        manager = self.helper.create_manager(manager_name='testmanager')
        payload = {
            'team_name': 'team1',
            'est_date': datetime.strptime('1900-01-05', '%Y-%m-%d').date(),
            'league': league.league_id,
            'stadium': stadium.stadium_id,
            'manager': manager.manager_id,
        }

        url = detail_url(team.team_id)
        res = self.staff_client.put(url, payload)
        team.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(team.team_name, payload['team_name'])
        self.assertEqual(team.est_date, payload['est_date'])
        self.assertEqual(team.league.league_id, payload['league'])
        self.assertEqual(team.stadium.stadium_id, payload['stadium'])
        self.assertEqual(team.manager.manager_id, payload['manager'])

    def test_full_update_by_normaluser_returns_error(self):
        """Test full update of team with normal user returns error."""
        team_name = 'My Team'
        team = self.helper.create_team(
            team_name=team_name,
        )
        league = self.helper.create_league(league_name='testleague')
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        manager = self.helper.create_manager(manager_name='testmanager')
        payload = {
            'team_name': 'team1',
            'est_date': datetime.strptime('1900-01-05', '%Y-%m-%d').date(),
            'league': league.league_id,
            'stadium': stadium.stadium_id,
            'manager': manager.manager_id,
        }

        url = detail_url(team.team_id)
        res = self.normal_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(team.team_name, team_name)

    def test_delete_team(self):
        """Test deleting a team successful."""
        team = self.helper.create_team(
            team_name='shakeel FC',
        )

        url = detail_url(team.team_id)
        res = self.staff_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(team_id=team.team_id).exists())

    def test_delete_team_by_normaluser_returns_error(self):
        """Test deleting a team with normal user returns error."""
        team_name = 'shakeel FC'
        team = self.helper.create_team(
            team_name=team_name,
        )

        url = detail_url(team.team_id)
        res = self.normal_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Team.objects.filter(team_id=team.team_id).exists())

    def test_retrieve_season_wise_team_stats_(self):
        """Test retrieving stats of a team for a specific season."""
        season = self.helper.create_season(
            season_name='2022-2023',
        )
        season1 = self.helper.create_season(
            season_name='2021-2022',
        )

        league = self.helper.create_league(
            league_name='my league',
        )
        team = self.helper.create_team(
            team_name='my team',
        )
        season_list = {'season': (season, 80), 'season1': (season1, 70)}
        for k, v in season_list.items():
            models.LeagueTable.objects.create(
                league=league,
                season=v[0],
                team=team,
                points=v[1],
                position=1,
                matches_played=34,
                matches_won=30,
                matches_drawn=4,
                matches_lost=0,
                goals_scored=90,
                goals_against=20,
                goal_difference=70,
            )

        url = stats_url(team.team_id, season.season_name)
        res = self.normal_client.get(url)
        serializer = TeamStatsSerializer(
            team, context={'season_name': season_list['season'][0].season_name},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.data['points'], 80)
        self.assertEqual(res.data['position'], 1)
        self.assertEqual(res.data['matches_played'], 34)
        self.assertEqual(res.data['matches_won'], 30)
        self.assertEqual(res.data['matches_drawn'], 4)
        self.assertEqual(res.data['matches_lost'], 0)
        self.assertEqual(res.data['goals_scored'], 90)
        self.assertEqual(res.data['goals_against'], 20)
        self.assertEqual(res.data['goal_difference'], 70)
