"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from goal_maven.core.managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=50, blank=False)
    last_name = models.CharField(_('Last Name'), max_length=50, blank=False)
    username = models.CharField(_('Username'), max_length=50, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    country = models.CharField(_('Country'), max_length=255, blank=True)
    favorite_team = models.CharField(_('Favorite Team'), max_length=255, blank=True)
    favorite_players = models.TextField(_('Favorite Players'), blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []


class Continent(models.Model):
    continent_id = models.AutoField(primary_key=True)
    continent_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.continent_name


class Nation(models.Model):
    nation_id = models.AutoField(primary_key=True)
    nation_name = models.CharField(max_length=50, blank=False)
    continent = models.ForeignKey('Continent', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.nation_name


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50, blank=False)
    nation = models.ForeignKey('Nation', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.city_name


class Stadium(models.Model):
    stadium_id = models.AutoField(primary_key=True)
    stadium_name = models.CharField(max_length=50, blank=False)
    city = models.ForeignKey('City', on_delete=models.CASCADE, blank=False)
    nation = models.ForeignKey('Nation', on_delete=models.CASCADE, blank=False)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.stadium_name


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, blank=False)
    est_date = models.DateField(blank=False)
    league = models.ForeignKey('League', on_delete=models.CASCADE, blank=False)
    stadium = models.ForeignKey('Stadium', on_delete=models.CASCADE, blank=False)
    manager = models.ForeignKey(
        'Manager', on_delete=models.CASCADE, blank=False, related_name='team_manager'
    )

    def __str__(self):
        return self.team_name


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='manager_of_team',
    )
    date_of_birth = models.DateField(blank=False)
    nation = models.ForeignKey('Nation', on_delete=models.CASCADE, blank=False)
    career_start = models.DateField(blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    jersy_number = models.SmallIntegerField(default=0, blank=True)
    date_of_birth = models.DateField(blank=False)
    nation = models.ForeignKey('Nation', on_delete=models.CASCADE, blank=False)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    role = models.ForeignKey('PlayerRole', on_delete=models.CASCADE, blank=False)
    total_appearances = models.IntegerField(default=0)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PlayerRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.role_name


class Referee(models.Model):
    referee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    nation = models.ForeignKey('Nation', on_delete=models.CASCADE, blank=False)
    career_start = models.DateField(blank=False)
    matches_officiated = models.SmallIntegerField(default=0)
    yellow_cards_issued = models.IntegerField(default=0)
    red_cards_issued = models.IntegerField(default=0)
    penalty_decisions_overturned = models.IntegerField(default=0)
    other_decisions_overturned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    season_name = models.CharField(max_length=50, blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    is_concluded = models.BooleanField(default=False)
    number_of_leagues = models.SmallIntegerField(default=0)
    number_of_matches = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    avg_goals_per_match = models.FloatField(default=0)

    def __str__(self):
        return self.season_name


class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    league_name = models.CharField(max_length=50, blank=False)
    nation = models.ForeignKey('Nation', on_delete=models.CASCADE, blank=False)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, blank=False)
    total_teams = models.SmallIntegerField(default=0)
    match_day = models.SmallIntegerField(default=0)
    top_scorer = models.ForeignKey(
        'Player', on_delete=models.CASCADE, blank=True, related_name='top_scorer'
    )
    most_assists = models.ForeignKey(
        'Player', on_delete=models.CASCADE, blank=True, related_name='most_assists'
    )
    is_concluded = models.BooleanField(default=False)
    champion_team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, blank=True, related_name='champion_team'
    )
    runner_up_team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, blank=True, related_name='runner_up_team'
    )

    def __str__(self):
        return self.league_name


class LeagueTable(models.Model):
    table_id = models.AutoField(primary_key=True)
    league = models.ForeignKey('League', on_delete=models.CASCADE, blank=False)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, blank=False)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=False)
    points = models.SmallIntegerField(default=0)
    position = models.SmallIntegerField(blank=True)
    matches_played = models.SmallIntegerField(default=0)
    matches_won = models.SmallIntegerField(default=0)
    matches_drawn = models.SmallIntegerField(default=0)
    maches_lost = models.SmallIntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"Team: {self.team}\nPosition: {self.position}\nPoints: {self.points}"


class Fixture(models.Model):
    fixture_id = models.AutoField(primary_key=True)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, blank=False)
    league = models.ForeignKey('League', on_delete=models.CASCADE, blank=False)
    match_day = models.SmallIntegerField(default=0)
    home_team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, blank=False, related_name='home_team'
    )
    away_team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, blank=False, related_name='away_team'
    )
    home_team_manager = models.ForeignKey(
        'Manager', on_delete=models.CASCADE, blank=False, related_name='home_manager'
    )
    away_team_manager = models.ForeignKey(
        'Manager', on_delete=models.CASCADE, blank=False, related_name='away_manager'
    )
    stadium = models.ForeignKey('Stadium', on_delete=models.CASCADE, blank=False)
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)
    referee = models.ForeignKey('Referee', on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    fixture = models.ForeignKey('Fixture', on_delete=models.CASCADE, blank=False)
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)
    stadium = models.ForeignKey('Stadium', on_delete=models.CASCADE, blank=False)
    attendance = models.IntegerField(default=0)
    referee = models.ForeignKey('Referee', on_delete=models.CASCADE, blank=False)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, blank=False)
    league = models.ForeignKey('League', on_delete=models.CASCADE, blank=False)
    result = models.BooleanField(default=False)
    winner_team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True)
    extra_time = models.BooleanField(default=False)
    injury_time = models.SmallIntegerField(default=0)
    home_team_goals = models.SmallIntegerField(default=0)
    away_team_goals = models.SmallIntegerField(default=0)
    home_team_possession = models.SmallIntegerField(default=0)
    away_team_possession = models.SmallIntegerField(default=0)
    home_team_shots = models.SmallIntegerField(default=0)
    away_team_shots = models.SmallIntegerField(default=0)
    home_team_shots_on_target = models.SmallIntegerField(default=0)
    away_team_shots_on_target = models.SmallIntegerField(default=0)
    home_team_shots_off_target = models.SmallIntegerField(default=0)
    away_team_shots_off_target = models.SmallIntegerField(default=0)
    home_team_shots_blocked = models.SmallIntegerField(default=0)
    away_team_shots_blocked = models.SmallIntegerField(default=0)
    home_team_corner_kicks = models.SmallIntegerField(default=0)
    away_team_corner_kicks = models.SmallIntegerField(default=0)
    home_team_offsides = models.SmallIntegerField(default=0)
    away_team_offsides = models.SmallIntegerField(default=0)
    home_team_fouls = models.SmallIntegerField(default=0)
    away_team_fouls = models.SmallIntegerField(default=0)
    home_team_throw_ins = models.SmallIntegerField(default=0)
    away_team_throw_ins = models.SmallIntegerField(default=0)
    home_team_yellow_cards = models.SmallIntegerField(default=0)
    away_team_yellow_cards = models.SmallIntegerField(default=0)
    home_team_red_cards = models.SmallIntegerField(default=0)
    away_team_red_cards = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.winner_team}"


class MatchEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_type = models.ForeignKey('EventType', on_delete=models.CASCADE, blank=False)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, blank=False)
    player = models.ForeignKey(
        'Player', on_delete=models.CASCADE, blank=False, related_name='player'
    )
    minute = models.SmallIntegerField(default=0)
    second = models.SmallIntegerField(default=0)
    is_extra_time = models.BooleanField(default=False)
    pitch_area = models.ForeignKey(
        'PitchLocation', on_delete=models.CASCADE, blank=False
    )
    associated_player = models.ForeignKey(
        'Player', on_delete=models.CASCADE, blank=False, related_name='associated_player'
    )

    def __str__(self):
        return f"{self.player} {self.event_type}"


class EventType(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.event_name


class PitchLocation(models.Model):
    pitch_area_id = models.AutoField(primary_key=True)
    pitch_area_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.pitch_area_name
