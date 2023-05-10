"""
This file contains helper methods for model testing.
"""
from django.core.exceptions import ObjectDoesNotExist

from goal_maven.core import models
from django.contrib.auth import get_user_model
from django.db import transaction

# import pdb
# import inspect


class HelperMethods:
    """Helper class containing methods to create objects for testing."""
    def __init__(self):
        self.staff_user = get_user_model().objects.create(
            email='teststaff@example.com',
            password='testpass123',
            first_name='test',
            last_name='staff',
            is_staff=True,
        )

    def create_continent(self, continent_name='test_continent'):
        """Method to create a continent."""
        with transaction.atomic():
            return models.Continent.objects.create(
                continent_name=continent_name,
                user=self.staff_user,
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
                user=self.staff_user,
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
                user=self.staff_user,
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
                user=self.staff_user,
            )

    def create_manager(self, first_name='test', last_name='manager', team=None):
        """Method to create a manager."""
        with transaction.atomic():
            if models.Nation.objects.count() > 0:
                nation = models.Nation.objects.first()
            else:
                nation = self.create_nation()
            return models.Manager.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth='1970-01-01',
                nation=nation,
                team=team,
                career_start='1995-01-01',
                user=self.staff_user,
            )

    def create_referee(self, first_name='test', last_name='referee'):
        """Method to create a referee."""
        with transaction.atomic():
            if models.Nation.objects.count() > 0:
                nation = models.Nation.objects.first()
            else:
                nation = self.create_nation()
            return models.Referee.objects.create(
                first_name=first_name,
                last_name=last_name,
                nation=nation,
                career_start='1995-01-01',
                user=self.staff_user,
            )

    def create_playerrole(self, role_name='test_role'):
        """Method to create a player role."""
        with transaction.atomic():
            return models.PlayerRole.objects.create(
                role_name=role_name,
                user=self.staff_user,
            )

    def create_player(self, first_name='test', last_name='player'):
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
                first_name=first_name,
                last_name=last_name,
                jersy_number='7',
                date_of_birth='1996-01-05',
                nation=nation,
                height=1.82,
                weight=96,
                role=role,
                total_appearances=100,
                career_start='1995-01-01',
                user=self.staff_user,
            )

    def create_season(self, season_name='test season'):
        """Method to create a season."""
        with transaction.atomic():
            return models.Season.objects.create(
                season_name=season_name,
                start_date='2022-01-01',
                end_date='2023-01-01',
                number_of_leagues=10,
                user=self.staff_user,
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
                user=self.staff_user,
            )

    def create_team(self, team_name='test'):
        """Method to create a team."""
        # print(inspect.stack()[1][3])
        with transaction.atomic():
            if models.League.objects.count() > 0:
                league = models.League.objects.first()
            else:
                league = self.create_league()
            if models.Stadium.objects.count() > 0:
                stadium = models.Stadium.objects.first()
            else:
                stadium = self.create_stadium()
            if len(models.Team.objects.all()) == len(models.Manager.objects.all()):
                manager = self.create_manager(
                    first_name='new',
                    last_name='manager',
                )
            team = models.Team.objects.create(
                team_name=team_name,
                est_date='1900-01-01',
                league=league,
                stadium=stadium,
                manager=manager,
                user=self.staff_user,
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
                user=self.staff_user,
            )

    def create_matchstatus(self, status_name='test_status'):
        """Method to create a match status."""
        with transaction.atomic():
            return models.MatchStatus.objects.create(
                status_name=status_name,
                user=self.staff_user,
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
            # pdb.set_trace()
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
                user=self.staff_user,
            )

    def create_match(self, home_team='team3', away_team='team4', fixture=None):
        """Method to create a match."""
        with transaction.atomic():
            if fixture:
                return models.Match.objects.create(
                    fixture=fixture,
                    user=self.staff_user,
                )
            else:
                fixture = self.create_fixture(
                    home_team=home_team,
                    away_team=away_team,
                )
            return models.Match.objects.create(
                fixture=fixture,
                user=self.staff_user,
            )

    # def create_matchevent(self, match=None):
    #     """Method to create a match event."""
    #     with transaction.atomic():
    #         if match:
    #             return models.Match.objects.create(
    #                 fixture=fixture,
    #                 user=self.staff_user,
    #             )
    #         else:
    #             fixture = self.create_fixture(
    #             home_team=home_team,
    #             away_team=away_team,
    #             )
    #         return models.Match.objects.create(
    #             fixture=fixture,
    #             user=self.staff_user,
    #         )
