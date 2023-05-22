"""
Tests for models.
"""
from datetime import date
from datetime import datetime
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import Client

from goal_maven.core import models
from goal_maven.core.tests.helper_methods import HelperMethods


class ModelTests(TestCase):
    """Test models."""

    def setUp(self):
        """Create admin user for test."""
        self.staff_client = Client()
        self.helper = HelperMethods()
        self.staff_user = self.helper.get_staff()

        self.staff_client.force_login(self.staff_user)
        self.user_client = Client()
        self.user = self.helper.get_user()
        self.user_client.force_login(self.user)

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        username = 'testuser123'
        date_of_birth = date(1996, 1, 5)
        first_name = 'test'
        last_name = 'user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com', 'test1user123'],
            ['Test2@Example.com', 'Test2@example.com', 'test2user123'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com', 'test3user123'],
            ['test4@example.COM', 'test4@example.com', 'test4user123'],
        ]
        date_of_birth = date(1996, 1, 5)
        for email, expected, username in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123',
                username=username,
                date_of_birth=date_of_birth,
                first_name='test',
                last_name='user',
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        country = self.helper.create_nation(
            nation_name='TestNation',
        )
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='test@example.com',
                password='test123',
                first_name='test',
                last_name='user',
                username='',
                country=country,
                date_of_birth=date(1996, 1, 5),
            )

    def test_new_user_with_correct_name_created(self):
        """Test user's first and last name is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        username = 'testuser123'
        date_of_birth = date(1996, 1, 5)
        first_name = 'test'
        last_name = 'user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_new_user_without_name_raises_error(self):
        """Test user's empty last name raises error."""
        email = 'test@example.com'
        password = 'testpass123'
        username = 'testuser123'
        date_of_birth = date(1996, 1, 5)
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                username=username,
                date_of_birth=date_of_birth,
            )

    def test_new_user_with_correct_username_created(self):
        """Test user's username is created correctly."""
        email = 'test@example.com'
        password = 'testpass123'
        username = 'testuser69'
        date_of_birth = date(1996, 1, 5)
        first_name = 'test'
        last_name = 'user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
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
        username = 'testuser69'
        date_of_birth = date(1996, 1, 5)
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
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
        username = 'testuser123'
        date_of_birth = datetime.now() + timedelta(days=1)
        date_of_birth = date_of_birth.date()
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                username=username,
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
        username = 'testuser123'
        date_of_birth = datetime.now() - timedelta(days=1824)
        date_of_birth = date_of_birth.date()
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                username=username,
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
        username = 'testuser123'
        date_of_birth = date(1996, 1, 5)
        team = self.helper.create_team(
            team_name='Real Madrid',
        )
        favorite_team = [team]
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
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
        username = 'testuser123'
        date_of_birth = date(1996, 1, 5)
        player1 = self.helper.create_player(
            player_name='Cristiano Ronaldo',
        )
        player2 = self.helper.create_player(
            player_name='Lionel Messi',
        )
        favorite_players = [player1, player2]
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
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
        username = 'testuser123'
        date_of_birth = date(1996, 1, 5)
        nation = self.helper.create_nation(
            nation_name='Pakistan',
        )
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
            country=nation,
        )

        self.assertEqual(user.country, nation)

    def test_update_user_details_is_successful(self):
        """Test updating user's details is successful."""
        email = 'test@example.com'
        username = 'testuser123'
        country = self.helper.create_nation(
            nation_name='Pakistan',
        )
        date_of_birth = date(1980, 1, 5)
        team1 = self.helper.create_team(
            team_name='team1'
        )
        team2 = self.helper.create_team(
            team_name='team2'
        )
        favorite_team = [team1, team2]
        player1 = self.helper.create_player(
            player_name='player1'
        )
        player2 = self.helper.create_player(
            player_name='player2'
        )
        favorite_players = [player1, player2]
        user = self.helper.create_user(
            email=email,
            username=username,
        )

        updated_password = 'updatedtestpass123'
        updated_first_name = 'updated_test'
        updated_last_name = 'updated_user'
        extra_fields = {
            'first_name': updated_first_name,
            'last_name': updated_last_name,
            'password': updated_password,
            'country': country,
            'date_of_birth': date_of_birth,
            'favorite_team': favorite_team,
            'favorite_players': favorite_players,
        }

        updated_user = get_user_model().objects.update_user(
            user=user,
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
            email='testsuper@example.com',
            password='test123',
            first_name='test',
            last_name='superuser',
            username='testsuper123',
            date_of_birth=date(1996, 1, 5),
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_continent_successful(self):
        """Test creating a continent with staff user is successful."""
        name = 'Asia'
        continent = self.helper.create_continent(name)

        self.assertEqual(models.Continent.objects.count(), 1)
        self.assertEqual(continent.continent_name, name)

    def test_create_continent_already_exists_error(self):
        """Test creating a continent which is already there raises error."""
        name = 'Australia'
        self.helper.create_continent(name)
        with self.assertRaises(IntegrityError):
            self.helper.create_continent(name)
        self.assertEqual(models.Continent.objects.count(), 1)

    def test_create_nation_successful(self):
        """Test creating a nation with staff user is successful."""
        name = 'Spain'
        nation = self.helper.create_nation(name)

        self.assertEqual(models.Nation.objects.count(), 1)
        self.assertEqual(nation.nation_name, name)

    def test_create_nation_already_exists_error(self):
        """Test creating a nation which is already there raises error."""
        name = 'Spain'
        self.helper.create_nation(name)
        with self.assertRaises(IntegrityError):
            self.helper.create_nation(name)
        self.assertEqual(models.Nation.objects.count(), 1)

    def test_create_stadium_successful(self):
        """Test creating a stadium with staff user is successful."""
        name = 'bernabeu'
        stadium = self.helper.create_stadium(name)

        self.assertEqual(models.Stadium.objects.count(), 1)
        self.assertEqual(stadium.stadium_name, name)

    def test_create_manager_successful(self):
        """Test creating a manager with staff user is successful."""
        name = 'Junaid'
        manager = self.helper.create_manager(
            manager_name=name,
        )

        self.assertEqual(models.Manager.objects.count(), 1)
        self.assertEqual(manager.manager_name, name)

    def test_create_referee_successful(self):
        """Test creating a referee with staff user is successful."""
        referee_name = 'Junaid'
        referee = self.helper.create_referee(
            referee_name=referee_name,
        )

        self.assertEqual(models.Referee.objects.count(), 1)
        self.assertEqual(referee.referee_name, referee_name)

    def test_create_playerrole_successful(self):
        """Test creating a player role with staff user is successful."""
        name = 'Striker'
        playerrole = self.helper.create_playerrole(name)

        self.assertEqual(models.PlayerRole.objects.count(), 1)
        self.assertEqual(playerrole.role_name, name)

    def test_create_player_successful(self):
        """Test creating a player with staff user is successful."""
        player_name = 'Junaid Malik'
        player = self.helper.create_player(
            player_name=player_name,
        )

        self.assertEqual(models.Player.objects.count(), 1)
        self.assertEqual(player.player_name, player_name)

    def test_create_season_successful(self):
        """Test creating a season with staff user is successful."""
        name = '22-23'
        season = self.helper.create_season(name)

        self.assertEqual(models.Season.objects.count(), 1)
        self.assertEqual(season.season_name, name)

    def test_create_league_successful(self):
        """Test creating a league with staff user is successful."""
        name = 'LaLiga Santander'
        league = self.helper.create_league(name)

        self.assertEqual(models.League.objects.count(), 1)
        self.assertEqual(league.league_name, name)

    def test_create_team_successful(self):
        """Test creating a team with staff user is successful."""
        name = 'Real Madrid'
        team = self.helper.create_team(name)

        self.assertEqual(models.Team.objects.count(), 1)
        self.assertEqual(team.team_name, name)

    def test_create_leaguetable_successful(self):
        """Test creating a league table entry with staff user is successful."""
        name = 'Real Madrid'
        points = 90
        position = 1
        leaguetable = self.helper.create_leaguetable(
            team_name=name,
            points=points,
            position=position,
        )

        self.assertEqual(models.LeagueTable.objects.count(), 1)
        self.assertEqual(leaguetable.team.team_name, name)

    def test_create_matchstatus_successful(self):
        """Test creating a match status with staff user is successful."""
        status = 'Scheduled'
        match_status = self.helper.create_matchstatus(
            status_name=status,
        )

        self.assertEqual(models.MatchStatus.objects.count(), 1)
        self.assertEqual(match_status.status_name, status)

    def test_create_fixture_successful(self):
        """Test creating a fixture with staff user is successful."""
        home_team = 'Real Madrid'
        away_team = 'Barcelona'
        fixture = self.helper.create_fixture(
            home_team=home_team,
            away_team=away_team,
        )

        self.assertEqual(models.Fixture.objects.count(), 1)
        self.assertEqual(fixture.home_team.team_name, home_team)
        self.assertEqual(fixture.away_team.team_name, away_team)

    def test_create_match_successful(self):
        """Test creating a match with staff user is successful."""
        home_team = 'Real Madrid'
        away_team = 'Barcelona'
        fixture = self.helper.create_fixture(
            home_team=home_team,
            away_team=away_team,
        )

        match = self.helper.create_match(fixture=fixture)

        self.assertEqual(models.Match.objects.count(), 1)
        self.assertEqual(match.fixture.home_team.team_name, home_team)
        self.assertEqual(match.fixture.away_team.team_name, away_team)

    def test_create_eventtype_successful(self):
        """Test creating an event type with staff user is successful."""
        name = 'Goal'
        event_type = self.helper.create_eventtype(
            event_name=name,
        )

        self.assertEqual(models.EventType.objects.count(), 1)
        self.assertEqual(event_type.event_name, name)

    def test_create_pitchposition_successful(self):
        """Test creating a pitchposition with staff user is successful."""
        name = 'Right channel'
        pitch_area = self.helper.create_pitchposition(
            pitch_area_name=name,
        )

        self.assertEqual(models.PitchLocation.objects.count(), 1)
        self.assertEqual(pitch_area.pitch_area_name, name)

    def test_create_matchevent_successful(self):
        """Test creating a match event with staff user is successful."""
        event_name = 'Foul'
        player = 'David Alaba'
        associated_player = 'Robert Lewandowski'
        minute = 59
        second = 20

        match_event = self.helper.create_matchevent(
            event_type=event_name,
            player=player,
            associated_player=associated_player,
            minute=minute,
            second=second,
        )

        self.assertEqual(models.MatchEvent.objects.count(), 1)
        self.assertEqual(match_event.event_type.event_name, event_name)
        self.assertEqual(match_event.player.player_name, player)
        self.assertEqual(
            match_event.associated_player.player_name, associated_player
        )
