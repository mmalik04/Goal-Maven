"""
This command populates database with sample data.
"""
from django.core.management.base import BaseCommand
# from faker import Faker
from goal_maven.core import models

import random
import time
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate sample data in the database'

    def handle(self, *args, **options):
        # fake = Faker()
        self.continents()
        self.nations()
        self.cities()
        self.stadiums()
        self.managers()
        self.referees()
        self.playerroles()
        self.players()
        self.seasons()
        self.leagues()
        # self.delete_all('League')
        self.stdout.write(self.style.SUCCESS('All done.'))

    def continents(self):
        self.stdout.write('Populating continents')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/continents.txt') as f:
            lines = f.readlines()
        for item in lines:
            continent_exist = models.Continent.objects.filter(
                continent_name=item.strip(),
            ).exists()
            if not continent_exist:
                models.Continent.objects.create(
                    continent_name=item.strip(),
                )
        self.stdout.write(self.style.SUCCESS('Continents have been populated.'))

    def nations(self):
        self.stdout.write('Populating nations')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/nations.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            nation_exist = models.Nation.objects.filter(
                nation_name=data[0].strip(),
            ).exists()
            if not nation_exist:
                continent = models.Continent.objects.get(
                    continent_name=data[1].strip(),
                )
                models.Nation.objects.create(
                    nation_name=data[0].strip(),
                    continent=continent,
                )
        self.stdout.write(self.style.SUCCESS('Nations have been populated.'))

    def cities(self):
        self.stdout.write('Populating cities')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/cities.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            city_exist = models.City.objects.filter(
                city_name=data[1].strip(),
            ).exists()
            if not city_exist:
                nation_exist = models.Nation.objects.filter(
                    nation_name=data[0].strip(),
                ).exists()
                if nation_exist:
                    nation = models.Nation.objects.get(
                        nation_name=data[0].strip(),
                    )
                    models.City.objects.create(
                        city_name=data[1].strip(),
                        nation=nation,
                    )
        self.stdout.write(self.style.SUCCESS('Cities have been populated.'))

    def stadiums(self):
        self.stdout.write('Populating stadiums')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/stadiums.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            stadium_exist = models.Stadium.objects.filter(
                stadium_name=data[0].strip(),
            ).exists()
            if not stadium_exist:
                city_exist = models.City.objects.filter(
                    city_name=data[1].strip(),
                ).exists()
                if city_exist:
                    city = models.City.objects.get(
                        city_name=data[1].strip(),
                    )
                    models.Stadium.objects.create(
                        stadium_name=data[0].strip(),
                        capacity=int(data[2].strip()),
                        city=city,
                    )
        self.stdout.write(self.style.SUCCESS('Stadiums have been populated.'))

    def managers(self):
        self.stdout.write('Populating managers')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/managers.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            manager_exist = models.Manager.objects.filter(
                manager_name=data[0].strip(),
            ).exists()
            if not manager_exist:
                nation_exist = models.Nation.objects.filter(
                    nation_name=data[1].strip(),
                ).exists()
                if nation_exist:
                    nation = models.Nation.objects.get(
                        nation_name=data[1].strip(),
                    )
                    career_start = self.helper_random_date(
                        '1970-01-01',
                        '1980-01-01',
                        random.random(),
                    )
                    date_of_birth = datetime.now() - timedelta(
                        days=int(data[2].strip())*365,
                    )

                    models.Manager.objects.create(
                        manager_name=data[0].strip(),
                        nation=nation,
                        career_start=career_start,
                        date_of_birth=date_of_birth.date(),
                    )
        self.stdout.write(self.style.SUCCESS('Managers have been populated.'))

    def referees(self):
        self.stdout.write('Populating referees')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/referees.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            referee_exist = models.Referee.objects.filter(
                referee_name=data[0].strip(),
            ).exists()
            if not referee_exist:
                nation_exist = models.Nation.objects.filter(
                    nation_name=data[1].strip(),
                ).exists()
                if nation_exist:
                    nation = models.Nation.objects.get(
                        nation_name=data[1].strip(),
                    )
                    career_start = self.helper_random_date(
                        '1990-01-01',
                        '1995-01-01',
                        random.random(),
                    )
                    matches_officiated = self.helper_random_number(50, 250)
                    yellow_cards_issued = self.helper_random_number(
                        matches_officiated,
                        matches_officiated*3,
                    )
                    red_cards_issued = self.helper_random_number(
                        matches_officiated-40,
                        matches_officiated-30,
                    )
                    penalty_decisions_overturned = self.helper_random_number(
                        5,
                        30,
                    )
                    other_decisions_overturned = self.helper_random_number(
                        10,
                        50,
                    )

                    models.Referee.objects.create(
                        referee_name=data[0].strip(),
                        nation=nation,
                        career_start=career_start,
                        matches_officiated=matches_officiated,
                        yellow_cards_issued=yellow_cards_issued,
                        red_cards_issued=red_cards_issued,
                        penalty_decisions_overturned=penalty_decisions_overturned,
                        other_decisions_overturned=other_decisions_overturned,
                    )
        self.stdout.write(self.style.SUCCESS('Referees have been populated.'))

    def playerroles(self):
        self.stdout.write('Populating Player roles')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/playerroles.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            role_exist = models.PlayerRole.objects.filter(
                role_name=data[0].strip(),
            ).exists()
            if not role_exist:
                models.PlayerRole.objects.create(
                    role_name=data[0].strip(),
                    role_key=data[1].strip(),
                )
        self.stdout.write(self.style.SUCCESS('Player roles have been populated.'))

    def players(self):
        self.stdout.write('Populating Players')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/players.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            player_exist = models.Player.objects.filter(
                player_name=data[1].strip(),
            ).exists()
            if not player_exist:
                nation_exist = models.Nation.objects.filter(
                    nation_name=data[4].strip(),
                ).exists()
                if nation_exist:
                    nation = models.Nation.objects.get(
                        nation_name=data[4].strip(),
                    )
                    team_exist = models.Team.objects.filter(
                        team_name=data[3].strip(),
                    ).exists()
                    if team_exist:
                        team = models.Team.objects.get(
                            team_name=data[3].strip(),
                        )
                    else:
                        team = None
                    jersy_number = data[0].strip()
                    date_of_birth = self.helper_random_date(
                        '1990-01-01',
                        '2003-01-01',
                        random.random(),
                    )
                    career_start = self.helper_random_date(
                        '2005-01-01',
                        '2017-01-01',
                        random.random(),
                    )
                    height = 1.82
                    weight = self.helper_random_number(60, 85)
                    role = models.PlayerRole.objects.get(
                        role_key=data[2].strip(),
                    )
                    total_appearances = self.helper_random_number(50, 300)

                    models.Player.objects.create(
                        player_name=data[1].strip(),
                        jersy_number=jersy_number,
                        nation=nation,
                        date_of_birth=date_of_birth,
                        career_start=career_start,
                        height=height,
                        weight=weight,
                        role=role,
                        total_appearances=total_appearances,
                        team=team,
                    )
        self.stdout.write(self.style.SUCCESS('Players have been populated.'))

    def seasons(self):
        self.stdout.write('Populating Seasons')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/seasons.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            season_name = data[0].strip()
            season_exist = models.Season.objects.filter(
                season_name=season_name,
            ).exists()
            if not season_exist:
                start_date = datetime.strptime(data[1].strip(), '%Y-%m-%d')
                end_date = datetime.strptime(data[2].strip(), '%Y-%m-%d')
                is_concluded = data[3].strip().lower() == 'true'
                number_of_leagues = int(data[4].strip())
                number_of_matches = int(data[5].strip())
                goals_scored = int(data[6].strip())
                avg_goals_per_match = float(data[7].strip())
                models.Season.objects.create(
                    season_name=season_name,
                    start_date=start_date,
                    end_date=end_date,
                    is_concluded=is_concluded,
                    number_of_leagues=number_of_leagues,
                    number_of_matches=number_of_matches,
                    goals_scored=goals_scored,
                    avg_goals_per_match=avg_goals_per_match,
                )
        self.stdout.write(self.style.SUCCESS('Seasons have been populated.'))

    def leagues(self):
        self.stdout.write('Populating Leagues')
        with open(r'/Goal-Maven/goal_maven/core/tests/test_data/leagues.txt') as f:
            lines = f.readlines()
        for item in lines:
            data = item.split('|')
            league_name = data[0].strip()
            season_name = data[2].strip()
            season = models.Season.objects.get(
                season_name=season_name,
            )
            league_exist = models.League.objects.filter(
                league_name=league_name,
                season=season,
            ).exists()
            if not league_exist:
                nation_exist = models.Nation.objects.filter(
                    nation_name=data[1].strip(),
                ).exists()
                if nation_exist:
                    nation = models.Nation.objects.get(
                        nation_name=data[1].strip(),
                    )
                    season = models.Season.objects.get(
                        season_name=season_name,
                    )
                    if data[5].strip().lower() == "none":
                        top_scorer = None
                    else:
                        top_scorer = models.Player.objects.get(
                            player_name=data[5].strip(),
                        )
                    if data[6].strip().lower() == "none":
                        most_assists = None
                    else:
                        most_assists = models.Player.objects.get(
                            player_name=data[6].strip(),
                        )
                    total_teams = data[3].strip()
                    match_day = data[4].strip()
                    is_concluded = data[7].strip().lower() == 'true'
                    champion_team_exist = models.Team.objects.filter(
                        team_name=data[8].strip(),
                    ).exists()
                    if champion_team_exist:
                        champion_team = models.Team.objects.get(
                            team_name=data[8].strip(),
                        )
                    else:
                        champion_team = None
                    runner_up_team_exist = models.Team.objects.filter(
                        team_name=data[9].strip(),
                    ).exists()
                    if runner_up_team_exist:
                        champion_team = models.Team.objects.get(
                            team_name=data[9].strip(),
                        )
                    else:
                        runner_up_team = None

                    models.League.objects.create(
                        league_name=league_name,
                        nation=nation,
                        season=season,
                        total_teams=total_teams,
                        match_day=match_day,
                        top_scorer=top_scorer,
                        most_assists=most_assists,
                        is_concluded=is_concluded,
                        champion_team=champion_team,
                        runner_up_team=runner_up_team,
                    )
        self.stdout.write(self.style.SUCCESS('Leagues have been populated.'))

    def helper_random_date(self, start, end, prop):
        time_format = '%Y-%m-%d'
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(time_format, time.localtime(ptime))

    def helper_random_number(self, start, end):
        return random.randint(start, end)

    def delete_all(self, model_to_del=None):
        self.stdout.write(f'Deleting all {model_to_del} objects.')
        if model_to_del:
            exec(f'models.{model_to_del}.objects.all().delete()')
