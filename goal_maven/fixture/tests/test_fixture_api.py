"""
Tests for Fixture APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from goal_maven.core.models import Match, Fixture
# from goal_maven.core import models

from goal_maven.core.tests.helper_methods import HelperMethods

from goal_maven.fixture.serializers import (
    FixtureSerializer,
    FixtureDetailSerializer,
    MatchSerializer,
    MatchDetailSerializer,
)

# from datetime import date, time

# from django.core.management import call_command
# import pdb


def fixtures_url(season_name):
    """Create and return a fixture list URL."""
    return reverse('fixture:fixture-list', args=[season_name])


def matches_url(season_name):
    """Create and return a match list URL."""
    return reverse('fixture:match-list', args=[season_name])


def detail_url_fixture(fixture_id):
    """Create and return a fixture detail URL."""
    return reverse('fixture:fixture-detail', args=[fixture_id])


def detail_url_match(match_id):
    """Create and return a match detail URL."""
    return reverse('fixture:match-detail', args=[match_id])


class PublicFixtureAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.helper = HelperMethods()

    def test_auth_required(self):
        """Test auth is required to call API."""
        season = self.helper.create_season('testseason')
        fixture = self.helper.create_fixture(season=season)
        res = self.client.get(fixtures_url(season.season_name))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.helper.create_match(fixture=fixture)


class PrivateFixtureApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.staff_client = APIClient()
        self.normal_client = APIClient()
        self.helper = HelperMethods()
        self.staff_user = self.helper.get_staff()
        self.normal_user = self.helper.get_user()
        self.staff_client.force_authenticate(self.staff_user)
        self.normal_client.force_authenticate(self.normal_user)

    def test_retrieve_fixtures(self):
        """Test retrieving a list of fixtures."""
        season = self.helper.create_season(season_name='season1')
        league = self.helper.create_league(
            league_name='league1',
            season=season,
        )
        self.helper.create_fixture(league=league, season=season)
        self.helper.create_fixture(league=league, season=season)

        res = self.normal_client.get(fixtures_url(season.season_name))

        fixtures = Fixture.objects.filter(season=season)
        serializer = FixtureSerializer(fixtures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_matches(self):
        """Test retrieving a list of matches."""
        season = self.helper.create_season(season_name='season2')
        league = self.helper.create_league(
            league_name='league2',
            season=season,
        )
        fixture1 = self.helper.create_fixture(league=league, season=season)
        fixture2 = self.helper.create_fixture(league=league, season=season)

        res = self.normal_client.get(matches_url(season.season_name))

        matches = Match.objects.filter(fixture__in=[fixture1, fixture2])
        serializer = MatchSerializer(matches, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_fixture_detail(self):
        """Test get fixture detail."""
        season = self.helper.create_season(season_name='season3')
        league = self.helper.create_league(league_name='league3', season=season)
        fixture = self.helper.create_fixture(league=league, season=season)

        res = self.normal_client.get(detail_url_fixture(fixture.fixture_id))

        serializer = FixtureDetailSerializer(fixture)
        self.assertEqual(res.data, serializer.data)

    def test_get_match_detail(self):
        """Test get match detail."""
        season = self.helper.create_season(season_name='season4')
        league = self.helper.create_league(league_name='league4', season=season)
        fixture = self.helper.create_fixture(league=league, season=season)
        match = self.helper.create_match(fixture=fixture)

        res = self.normal_client.get(detail_url_match(match.match_id))

        serializer = MatchDetailSerializer(match)
        self.assertEqual(res.data, serializer.data)

    def test_create_fixture(self):
        """Test creating a fixture."""
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        referee = self.helper.create_referee(referee_name='testreferee')
        season = self.helper.create_season(season_name='season3')
        league = self.helper.create_league(league_name='league3', season=season)
        home_manager = self.helper.create_manager(manager_name='testmanager1')
        away_manager = self.helper.create_manager(manager_name='testmanager2')
        home_team = self.helper.create_team(
            team_name='team1', stadium=stadium, manager=home_manager,
            league=league,
        )
        away_team = self.helper.create_team(team_name='team2', manager=away_manager)
        my_date = '2023-06-01'
        my_time = '20:00'
        match_status = self.helper.create_matchstatus(status_name='Scheduled')
        payload = {
            'season': season.season_id,
            'league': league.league_id,
            'match_day': 1,
            'home_team': home_team.team_id,
            'away_team': away_team.team_id,
            'home_team_manager': home_manager.manager_name,
            'away_team_manager': away_manager.manager_name,
            'stadium': stadium.stadium_id,
            'date': my_date,
            'time': my_time,
            'referee': referee.referee_id,
            'match_status': match_status.match_status_id,
        }
        res = self.staff_client.post(fixtures_url(season.season_name), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        fixture = Fixture.objects.get(fixture_id=res.data['fixture_id'])
        match = Match.objects.get(fixture=fixture)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Fixture.objects.filter(fixture_id=res.data['fixture_id']).exists()
        )
        self.assertEqual(fixture.season, season)
        self.assertEqual(fixture.league, league)
        self.assertEqual(fixture.home_team, home_team)
        self.assertEqual(fixture.away_team, away_team)
        self.assertEqual(match.fixture, fixture)

    def test_create_match_returns_error(self):
        """Test creating a match returns error."""
        fixture = self.helper.create_fixture()
        payload = {
            'fixture': fixture.fixture_id,
        }

        res = self.normal_client.post(matches_url(fixture.season.season_name), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_fixture_by_normaluser_returns_error(self):
        """Test creating a fixture with normal user returns error."""
        stadium = self.helper.create_stadium(stadium_name='teststadium')
        referee = self.helper.create_referee(referee_name='testreferee')
        season = self.helper.create_season(season_name='season3')
        league = self.helper.create_league(league_name='league3', season=season)
        home_manager = self.helper.create_manager(manager_name='testmanager1')
        away_manager = self.helper.create_manager(manager_name='testmanager2')
        home_team = self.helper.create_team(
            team_name='team1', stadium=stadium, manager=home_manager,
            league=league,
        )
        away_team = self.helper.create_team(team_name='team2', manager=away_manager)
        my_date = '2023-06-01'
        my_time = '20:00'
        match_status = self.helper.create_matchstatus(status_name='Scheduled')
        payload = {
            'season': season.season_id,
            'league': league.league_id,
            'match_day': 1,
            'home_team': home_team.team_id,
            'away_team': away_team.team_id,
            'home_team_manager': home_manager.manager_name,
            'away_team_manager': away_manager.manager_name,
            'stadium': stadium.stadium_id,
            'date': my_date,
            'time': my_time,
            'referee': referee.referee_id,
            'match_status': match_status.match_status_id,
        }

        res = self.normal_client.post(fixtures_url(season.season_name), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_fixture(self):
        """Test partial update of a fixture."""
        my_time = '22:00'
        season = self.helper.create_season(season_name='test season')
        league = self.helper.create_league(season=season)
        fixture = self.helper.create_fixture(league=league, season=season)

        payload = {'time': my_time}
        url = detail_url_fixture(fixture.fixture_id)
        res = self.staff_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        fixture.refresh_from_db()
        self.assertEqual(fixture.time.strftime('%H:%M'), payload['time'])

    def test_partial_update_match(self):
        """Test partial update of a match."""
        fixture = self.helper.create_fixture()
        match = self.helper.create_match(fixture=fixture)

        payload = {'home_team_goals': 2}
        url = detail_url_match(match.match_id)
        res = self.staff_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        match.refresh_from_db()
        self.assertEqual(match.home_team_goals, payload['home_team_goals'])

    def test_partial_update_fixture_by_normaluser_returns_error(self):
        """Test partial update fixture with normal user returns error."""
        my_time = '22:00'
        season = self.helper.create_season(season_name='test season')
        league = self.helper.create_league(season=season)
        fixture = self.helper.create_fixture(league=league, season=season)

        payload = {'time': my_time}
        url = detail_url_fixture(fixture.fixture_id)

        res = self.normal_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_match_by_normaluser_returns_error(self):
        """Test partial update match with normal user returns error."""
        fixture = self.helper.create_fixture()
        match = self.helper.create_match(fixture=fixture)

        payload = {'home_team_goals': 2}
        url = detail_url_match(match.match_id)

        res = self.normal_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_fixture(self):
        """Test full update of fixture."""
        fixture = self.helper.create_fixture()

        stadium = self.helper.create_stadium(stadium_name='teststadium')
        referee = self.helper.create_referee(referee_name='testreferee')
        season = self.helper.create_season(season_name='season3')
        league = self.helper.create_league(league_name='league3', season=season)
        home_manager = self.helper.create_manager(manager_name='testmanager1')
        away_manager = self.helper.create_manager(manager_name='testmanager2')
        home_team = self.helper.create_team(
            team_name='myteam1', stadium=stadium, manager=home_manager,
            league=league,
        )
        away_team = self.helper.create_team(team_name='myteam2', manager=away_manager)
        my_date = '2023-06-01'
        my_time = '20:00'
        match_status = self.helper.create_matchstatus(status_name='Scheduled')
        payload = {
            'season': season.season_id,
            'league': league.league_id,
            'match_day': 1,
            'home_team': home_team.team_id,
            'away_team': away_team.team_id,
            'home_team_manager': home_manager.manager_name,
            'away_team_manager': away_manager.manager_name,
            'stadium': stadium.stadium_id,
            'date': my_date,
            'time': my_time,
            'referee': referee.referee_id,
            'match_status': match_status.match_status_id,
        }

        url = detail_url_fixture(fixture.fixture_id)
        res = self.staff_client.put(url, payload)
        fixture.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(fixture.home_team.team_id, payload['home_team'])
        self.assertEqual(fixture.away_team.team_id, payload['away_team'])
        self.assertEqual(fixture.season.season_id, payload['season'])
        self.assertEqual(fixture.league.league_id, payload['league'])

    def test_full_update_match(self):
        """Test full update of match."""
        fixture = self.helper.create_fixture()
        match = self.helper.create_match(fixture=fixture)

        payload = {
            'fixture': fixture.fixture_id,
            'home_team_goals': 2,
            'away_team_goals': 1,
            'home_team_yellow_cards': 1,
            'away_team_yellow_cards': 2,
            'home_team_red_cards': 1,
            'away_team_red_cards': 0,
            'home_team_penalties': 1,
            'away_team_penalties': 0,
            'home_team_possession': 60,
            'away_team_possession': 40,
            'home_team_shots': 10,
            'away_team_shots': 5,
            'home_team_shots_on_target': 5,
            'away_team_shots_on_target': 3,
            'home_team_corners': 5,
            'away_team_corners': 3,
            'home_team_fouls': 10,
            'away_team_fouls': 5,
            'home_team_offsides': 2,
            'away_team_offsides': 1,
            'home_team_shots_off_target': 5,
            'away_team_shots_off_target': 2,
            'home_team_shots_blocked': 0,
            'away_team_shots_blocked': 0,
            'home_team_corner_kicks': 5,
            'away_team_corner_kicks': 3,
            'home_team_throw_ins': 10,
            'away_team_throw_ins': 5,
            'extra_time': False,
            'injury_time': 10,
            'result': True,
            'attendance': 10000,
            'winner_team': fixture.home_team.team_id,
        }

        url = detail_url_match(match.match_id)
        res = self.staff_client.put(url, payload)
        match.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(match.home_team_goals, payload['home_team_goals'])
        self.assertEqual(match.away_team_goals, payload['away_team_goals'])
        self.assertEqual(match.winner_team.team_id, payload['winner_team'])

    def test_full_update_fixture_by_normaluser_returns_error(self):
        """Test full update of fixture with normal user returns error."""
        fixture = self.helper.create_fixture(
            home_team='team1',
            away_team='team2',
        )

        stadium = self.helper.create_stadium(stadium_name='teststadium')
        referee = self.helper.create_referee(referee_name='testreferee')
        season = self.helper.create_season(season_name='season3')
        league = self.helper.create_league(league_name='league3', season=season)
        home_manager = self.helper.create_manager(manager_name='testmanager1')
        away_manager = self.helper.create_manager(manager_name='testmanager2')
        home_team = self.helper.create_team(
            team_name='myteam1', stadium=stadium, manager=home_manager,
            league=league,
        )
        away_team = self.helper.create_team(team_name='myteam2', manager=away_manager)
        my_date = '2023-06-01'
        my_time = '20:00'
        match_status = self.helper.create_matchstatus(status_name='Scheduled')
        payload = {
            'season': season.season_id,
            'league': league.league_id,
            'match_day': 1,
            'home_team': home_team.team_id,
            'away_team': away_team.team_id,
            'home_team_manager': home_manager.manager_name,
            'away_team_manager': away_manager.manager_name,
            'stadium': stadium.stadium_id,
            'date': my_date,
            'time': my_time,
            'referee': referee.referee_id,
            'match_status': match_status.match_status_id,
        }

        url = detail_url_fixture(fixture.fixture_id)
        res = self.normal_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(fixture.home_team.team_name, 'team1')
        self.assertEqual(fixture.away_team.team_name, 'team2')

    def test_full_update_match_by_normaluser_returns_error(self):
        """Test full update of match with normal user returns error."""
        fixture = self.helper.create_fixture()
        match = self.helper.create_match(fixture=fixture)

        payload = {
            'fixture': fixture.fixture_id,
            'home_team_goals': 2,
            'away_team_goals': 1,
            'home_team_yellow_cards': 1,
            'away_team_yellow_cards': 2,
            'home_team_red_cards': 1,
            'away_team_red_cards': 0,
            'home_team_penalties': 1,
            'away_team_penalties': 0,
            'home_team_possession': 60,
            'away_team_possession': 40,
            'home_team_shots': 10,
            'away_team_shots': 5,
            'home_team_shots_on_target': 5,
            'away_team_shots_on_target': 3,
            'home_team_corners': 5,
            'away_team_corners': 3,
            'home_team_fouls': 10,
            'away_team_fouls': 5,
            'home_team_offsides': 2,
            'away_team_offsides': 1,
            'home_team_shots_off_target': 5,
            'away_team_shots_off_target': 2,
            'home_team_shots_blocked': 0,
            'away_team_shots_blocked': 0,
            'home_team_corner_kicks': 5,
            'away_team_corner_kicks': 3,
            'home_team_throw_ins': 10,
            'away_team_throw_ins': 5,
            'extra_time': False,
            'injury_time': 10,
            'result': True,
            'attendance': 10000,
            'winner_team': fixture.home_team.team_id,
        }

        url = detail_url_match(match.match_id)
        res = self.normal_client.put(url, payload)
        match.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(match.home_team_goals, 0)
        self.assertEqual(match.away_team_goals, 0)
        self.assertEqual(match.winner_team, None)

    def test_delete_fixture(self):
        """Test deleting a fixture successful."""
        fixture = self.helper.create_fixture(
            home_team='team1',
            away_team='team2',
        )

        url = detail_url_fixture(fixture.fixture_id)
        res = self.staff_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Fixture.objects.filter(fixture_id=fixture.fixture_id).exists())

    def test_delete_match_returns_error(self):
        """Test deleting a match returns error."""
        fixture = self.helper.create_fixture()
        match = self.helper.create_match(fixture=fixture)

        url = detail_url_match(match.match_id)
        res = self.staff_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Match.objects.filter(match_id=match.match_id).exists())

    def test_delete_fixture_by_normaluser_returns_error(self):
        """Test deleting a fixture with normal user returns error."""
        fixture = self.helper.create_fixture(
            home_team='team1',
            away_team='team2',
        )

        url = detail_url_fixture(fixture.fixture_id)
        res = self.normal_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Fixture.objects.filter(fixture_id=fixture.fixture_id).exists())
