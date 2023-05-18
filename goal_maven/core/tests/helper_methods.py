"""
This file contains helper methods for model testing.
"""
from django.core.exceptions import ObjectDoesNotExist

from goal_maven.core import models
from django.contrib.auth import get_user_model
from django.db import transaction

from datetime import date

# import pdb
# import inspect
# import os


class HelperMethods:
    """Helper class containing methods to create objects for testing."""

    def __init__(self):
        self.staff_user = self.create_staff(email='staff@example.com')
        self.user = self.create_user(email='user@example.com')

    def get_staff(self):
        return self.staff_user

    def get_user(self):
        return self.user

    def create_staff(self, **params):
        if 'email' not in params:
            params['email'] = 'staff@example.com'
        staff_user_exists = get_user_model().objects.filter(
            email=params['email'],
        ).exists()
        if staff_user_exists:
            return get_user_model().objects.get(email=params['email'])
        if 'password' not in params:
            params['password'] = 'testpass123'
        if 'username' not in params:
            params['username'] = 'userstaff123'
        if 'date_of_birth' not in params:
            params['date_of_birth'] = date(1996, 1, 5)
        if 'first_name' not in params:
            params['first_name'] = 'User'
        if 'last_name' not in params:
            params['last_name'] = 'Staff'
        if 'country' not in params:
            params['country'] = None
        if 'favorite_team' not in params:
            params['favorite_team'] = None
        if 'favorite_players' not in params:
            params['favorite_players'] = None
        try:
            staff_user = get_user_model().objects.create(
                email=params['email'],
                password=params['password'],
                username=params['username'],
                date_of_birth=params['date_of_birth'],
                first_name=params['first_name'],
                last_name=params['last_name'],
                country=params['country'],
                favorite_team=params['favorite_team'],
                favorite_players=params['favorite_players'],
                is_staff=True
            )

            return staff_user
        except Exception as e:
            raise e

    def create_user(self, **params):
        if 'email' not in params:
            params['email'] = 'user@example.com'
        user_exists = get_user_model().objects.filter(
            email=params['email'],
        ).exists()
        if user_exists:
            return get_user_model().objects.get(email=params['email'])
        if 'password' not in params:
            params['password'] = 'testpass123'
        if 'username' not in params:
            params['username'] = 'usernormal123'
        if 'date_of_birth' not in params:
            params['date_of_birth'] = date(1996, 1, 5)
        if 'first_name' not in params:
            params['first_name'] = 'User'
        if 'last_name' not in params:
            params['last_name'] = 'Normal'
        if 'country' not in params:
            params['country'] = None
        if 'favorite_team' not in params:
            params['favorite_team'] = None
        if 'favorite_players' not in params:
            params['favorite_players'] = None
        try:
            user = get_user_model().objects.create(
                email=params['email'],
                password=params['password'],
                username=params['username'],
                date_of_birth=params['date_of_birth'],
                first_name=params['first_name'],
                last_name=params['last_name'],
                country=params['country'],
                favorite_team=params['favorite_team'],
                favorite_players=params['favorite_players'],
            )

            return user
        except Exception as e:
            raise e

    def create_continent(self, continent_name='test_continent'):
        """Method to create a continent."""
        with transaction.atomic():

            return models.Continent.objects.create(
                continent_name=continent_name,
            )

    def create_nation(self, nation_name='test_nation'):
        """Method to create a nation."""
        with transaction.atomic():
            if models.Continent.objects.count() > 0:
                continent = models.Continent.objects.first()
            else:
                continent = self.create_continent()

            return models.Nation.objects.create(
                nation_name=nation_name,
                continent=continent,
            )

    def create_city(self, city_name='test_city'):
        """Method to create a city."""
        with transaction.atomic():
            if models.Nation.objects.count() > 0:
                nation = models.Nation.objects.first()
            else:
                nation = self.create_nation()

            return models.City.objects.create(
                city_name=city_name,
                nation=nation,
            )

    def create_stadium(self, stadium_name='test_stadium'):
        """Method to create a stadium."""
        with transaction.atomic():
            if models.City.objects.count() > 0:
                city = models.City.objects.first()
            else:
                city = self.create_city()

            return models.Stadium.objects.create(
                stadium_name=stadium_name,
                city=city,
                capacity=90000,
            )

    def create_manager(self, manager_name='test manager', team=None):
        """Method to create a manager."""
        with transaction.atomic():
            if models.Nation.objects.count() > 0:
                nation = models.Nation.objects.first()
            else:
                nation = self.create_nation()

            return models.Manager.objects.create(
                manager_name=manager_name,
                date_of_birth='1970-01-01',
                nation=nation,
                team=team,
                career_start='1995-01-01',
            )

    def create_referee(self, referee_name='test referee'):
        """Method to create a referee."""
        with transaction.atomic():
            if models.Nation.objects.count() > 0:
                nation = models.Nation.objects.first()
            else:
                nation = self.create_nation()

            return models.Referee.objects.create(
                referee_name=referee_name,
                nation=nation,
                career_start='1995-01-01',
            )

    def create_playerrole(self, role_name='test_role', role_key='TT'):
        """Method to create a player role."""
        with transaction.atomic():

            return models.PlayerRole.objects.create(
                role_name=role_name,
                role_key=role_key,
            )

    def create_player(self, player_name='test player'):
        """Method to create a player."""
        with transaction.atomic():
            if models.Nation.objects.count() > 0:
                nation = models.Nation.objects.first()
            else:
                nation = self.create_nation()
            if models.PlayerRole.objects.count() > 0:
                role = models.PlayerRole.objects.first()
            else:
                role = self.create_playerrole()

            return models.Player.objects.create(
                player_name=player_name,
                jersy_number='7',
                date_of_birth='1996-01-05',
                nation=nation,
                height=1.82,
                weight=96,
                role=role,
                total_appearances=100,
                career_start='1995-01-01',
            )

    def create_season(self, season_name='test season'):
        """Method to create a season."""
        with transaction.atomic():

            return models.Season.objects.create(
                season_name=season_name,
                start_date='2022-01-01',
                end_date='2023-01-01',
                number_of_leagues=10,
            )

    def create_league(self, league_name='test'):
        """Method to create a league."""
        with transaction.atomic():
            if models.Nation.objects.count() > 0:
                nation = models.Nation.objects.first()
            else:
                nation = self.create_nation()
            if models.Season.objects.count() > 0:
                season = models.Season.objects.first()
            else:
                season = self.create_season()

            return models.League.objects.create(
                league_name=league_name,
                nation=nation,
                season=season,
            )

    def create_team(self, team_name='test'):
        """Method to create a team."""
        with transaction.atomic():
            if models.League.objects.count() > 0:
                league = models.League.objects.first()
            else:
                league = self.create_league()
            if models.Stadium.objects.count() > 0:
                stadium = models.Stadium.objects.first()
            else:
                stadium = self.create_stadium()
            if len(models.Team.objects.all()) <= len(models.Manager.objects.all()):
                manager = self.create_manager(
                    manager_name='new manager',
                )

            team = models.Team.objects.create(
                team_name=team_name,
                est_date='1900-01-01',
                league=league,
                stadium=stadium,
                manager=manager,
            )
            manager.team = team

            return team

    def create_leaguetable(self, team_name='Test Team', points=0, position=1):
        """Method to create a league table."""
        with transaction.atomic():
            if models.League.objects.count() > 0:
                league = models.League.objects.first()
            else:
                league = self.create_league()
            if models.Season.objects.count() > 0:
                season = models.Season.objects.first()
            else:
                season = self.create_season()
            try:
                team = models.Team.objects.get(team_name=team_name)
            except ObjectDoesNotExist:
                team = self.create_team(team_name)

            return models.LeagueTable.objects.create(
                league=league,
                season=season,
                team=team,
                points=points,
                position=position,
            )

    def create_matchstatus(self, status_name='test_status'):
        """Method to create a match status."""
        with transaction.atomic():

            return models.MatchStatus.objects.create(
                status_name=status_name,
            )

    def create_fixture(
            self, home_team='team1', away_team='team2',
            date='2023-01-01', time='20:00:00',
            ):
        """Method to create a fixture."""
        with transaction.atomic():
            if models.Season.objects.count() > 0:
                season = models.Season.objects.first()
            else:
                season = self.create_season()
            if models.League.objects.count() > 0:
                league = models.League.objects.first()
            else:
                league = self.create_league()
            if models.Stadium.objects.count() > 0:
                stadium = models.Stadium.objects.first()
            else:
                stadium = self.create_stadium()
            if models.Referee.objects.count() > 0:
                referee = models.Referee.objects.first()
            else:
                referee = self.create_referee()
            if models.MatchStatus.objects.count() > 0:
                match_status = models.MatchStatus.objects.first()
            else:
                match_status = self.create_matchstatus()
            try:
                home_team = models.Team.objects.get(team_name=home_team)
            except ObjectDoesNotExist:
                home_team = self.create_team(home_team)
            try:
                away_team = models.Team.objects.get(team_name=away_team)
            except ObjectDoesNotExist:
                away_team = self.create_team(away_team)

            return models.Fixture.objects.create(
                season=season,
                league=league,
                stadium=stadium,
                home_team=home_team,
                away_team=away_team,
                home_team_manager=str(home_team.manager),
                away_team_manager=str(away_team.manager),
                referee=referee,
                date=date,
                time=time,
                match_status=match_status,
            )

    def create_match(self, home_team='team3', away_team='team4', fixture=None):
        """Method to create a match."""
        with transaction.atomic():
            if fixture:

                return models.Match.objects.create(
                    fixture=fixture,
                )
            else:
                fixture = self.create_fixture(
                    home_team=home_team,
                    away_team=away_team,
                )

            return models.Match.objects.create(
                fixture=fixture,
            )

    def create_eventtype(self, event_name='test_event'):
        """Method to create a event type status."""
        with transaction.atomic():

            return models.EventType.objects.create(
                event_name=event_name,
            )

    def create_pitchposition(self, pitch_area_name='test_area'):
        """Method to create a pitch position status."""
        with transaction.atomic():
            pitchposition_exists = models.PitchLocation.objects.filter(
                pitch_area_name=pitch_area_name,
            ).exists()
            if not pitchposition_exists:

                return models.PitchLocation.objects.create(
                    pitch_area_name=pitch_area_name,
                )
            obj_count = models.PitchLocation.objects.count()

            return models.PitchLocation.objects.create(
                pitch_area_name=pitch_area_name+str(obj_count),
            )

    def create_matchevent(
            self, event_name='test event', player='test_player',
            associated_player='test_associatedplayer', minute=10,
            second=40,
            ):
        """Method to create a match event."""
        with transaction.atomic():
            event_exists = models.EventType.objects.filter(
                event_name=event_name,
            ).exists()
            if event_exists:
                event_type = models.EventType.objects.get(event_name=event_name)
            else:
                event_type = self.create_eventtype(event_name=event_name)
            match = self.create_match()
            player_exists = models.Player.objects.filter(
                player_name=player,
            ).exists()
            if player_exists:
                player = models.Player.objects.get(
                    player_name=player,
                )
            else:
                player = self.create_player(player_name=player)
            pitch_area = self.create_pitchposition()
            associated_player_exists = models.Player.objects.filter(
                player_name=associated_player,
            ).exists()
            if associated_player_exists:
                associated_player = models.Player.objects.get(
                    player_name=associated_player,
                )
            else:
                associated_player = self.create_player(
                    player_name=associated_player,
                )

            return models.MatchEvent.objects.create(
                event_type=event_type,
                match=match,
                player=player,
                minute=minute,
                second=second,
                pitch_area=pitch_area,
                associated_player=associated_player,
            )
