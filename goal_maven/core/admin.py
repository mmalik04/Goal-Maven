"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from goal_maven.core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name',
                    'date_of_birth']
    fieldsets = (
        (_('Details'), {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': (
            'first_name', 'last_name', 'username', 'date_of_birth',
            'country', 'groups',
        )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['last_login', 'date_joined']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


class ContinentAdmin(admin.ModelAdmin):
    """Define the admin pages for Continents."""

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    ordering = ['continent_id']
    list_display = ['continent_name']
    fieldsets = (
        (_('Details'), {'fields': ('continent_name', 'created_by')}),
    )
    readonly_fields = []


class NationAdmin(admin.ModelAdmin):
    """Define the admin pages for Nations."""
    ordering = ['nation_id']
    list_display = ['nation_name']
    fieldsets = (
        (_('Details'), {'fields': ('nation_name', 'continent')}),
    )
    readonly_fields = []


class CityAdmin(admin.ModelAdmin):
    """Define the admin pages for Cities."""
    ordering = ['city_id']
    list_display = ['city_name']
    fieldsets = (
        (_('Details'), {'fields': ('city_name', 'nation')}),
    )
    readonly_fields = []


class StadiumAdmin(admin.ModelAdmin):
    """Define the admin pages for Stadiums."""
    ordering = ['stadium_id']
    list_display = ['stadium_name', 'capacity', 'city']
    fieldsets = (
        (_('Details'), {'fields': ('stadium_name', 'capacity', 'city',)}),
    )
    readonly_fields = []


class TeamAdmin(admin.ModelAdmin):
    """Define the admin pages for Teams."""
    ordering = ['team_id']
    list_display = ['team_name', 'manager', 'league']
    fieldsets = (
        (_('Details'), {'fields': (
            'team_name', 'est_date', 'league', 'stadium', 'manager',
        )}),
    )
    readonly_fields = []


class ManagerAdmin(admin.ModelAdmin):
    """Define the admin pages for Managers."""
    ordering = ['manager_id']
    list_display = ['first_name', 'last_name', 'team', 'career_start']
    fieldsets = (
        (_('Details'), {'fields': (
            'first_name', 'last_name', 'team', 'date_of_birth', 'nation',
            'career_start',
        )}),
    )
    readonly_fields = []


class PlayerAdmin(admin.ModelAdmin):
    """Define the admin pages for Players."""
    ordering = ['player_id']
    list_display = ['first_name', 'last_name', 'team', 'jersy_number']
    fieldsets = (
        (_('Details'), {'fields': (
            'first_name', 'last_name', 'jersy_number', 'team', 'date_of_birth',
            'nation', 'height', 'weight', 'role', 'total_appearances',
        )}),
    )
    readonly_fields = []


class PlayerRoleAdmin(admin.ModelAdmin):
    """Define the admin pages for PlayerRoles."""
    ordering = ['role_id']
    list_display = ['role_name']
    fieldsets = (
        (_('Details'), {'fields': ('role_name',)}),
    )
    readonly_fields = []


class RefereeAdmin(admin.ModelAdmin):
    """Define the admin pages for Referees."""
    ordering = ['referee_id']
    list_display = ['first_name', 'last_name', 'nation', 'matches_officiated']
    fieldsets = (
        (_('Details'), {'fields': (
            'first_name', 'last_name', 'nation', 'career_start', 'matches_officiated',
            'yellow_cards_issued', 'red_cards_issued', 'penalty_decisions_overturned',
            'other_decisions_overturned',
        )}),
    )
    readonly_fields = []


class SeasonAdmin(admin.ModelAdmin):
    """Define the admin pages for Seasons."""
    ordering = ['season_id']
    list_display = ['season_name', 'start_date', 'end_date', 'is_concluded']
    fieldsets = (
        (_('Details'), {'fields': (
            'season_name', 'start_date', 'end_date', 'is_concluded', 'number_of_leagues',
            'number_of_matches', 'goals_scored', 'avg_goals_per_match',
        )}),
    )
    readonly_fields = []


class LeagueAdmin(admin.ModelAdmin):
    """Define the admin pages for Leagues."""
    ordering = ['league_id']
    list_display = ['league_name', 'nation', 'season', 'is_concluded', 'champion_team',
                    'top_scorer', 'most_assists']
    fieldsets = (
        (_('Details'), {'fields': (
            'league_name', 'nation', 'season', 'total_teams', 'match_day',
            'top_scorer', 'most_assists', 'is_concluded', 'champion_team',
            'runner_up_team',
        )}),
    )
    readonly_fields = []


class LeagueTableAdmin(admin.ModelAdmin):
    """Define the admin pages for LeagueTables."""
    ordering = ['table_id']
    list_display = ['position', 'team', 'points', 'matches_played', 'matches_won',
                    'matches_drawn', 'maches_lost', 'goal_difference']
    fieldsets = (
        (_('Details'), {'fields': (
            'league', 'season', 'team', 'points', 'position',
            'matches_played', 'matches_won', 'matches_drawn', 'maches_lost',
            'goals_scored', 'goals_against', 'goal_difference',
        )}),
    )
    readonly_fields = []


class FixtureAdmin(admin.ModelAdmin):
    """Define the admin pages for Fixtures."""
    ordering = ['fixture_id']
    list_display = ['match_day', 'home_team', 'away_team', 'time', 'date',
                    'match_status']
    fieldsets = (
        (_('Details'), {'fields': (
            'season', 'league', 'match_day', 'home_team', 'away_team',
            'home_team_manager', 'away_team_manager', 'stadium', 'date',
            'time', 'referee', 'match_status',
        )}),
    )
    readonly_fields = []


class MatchAdmin(admin.ModelAdmin):
    """Define the admin pages for Matches."""
    ordering = ['match_id']
    list_display = ['fixture', 'result', 'winner_team']
    fieldsets = (
        (_('Details'), {'fields': (
            'fixture', 'attendance',
            'result', 'winner_team', 'extra_time', 'injury_time',
            'home_team_goals', 'away_team_goals', 'home_team_possession',
            'away_team_possession', 'home_team_shots', 'away_team_shots',
            'home_team_shots_on_target', 'away_team_shots_on_target',
            'home_team_shots_off_target', 'away_team_shots_off_target',
            'home_team_shots_blocked', 'away_team_shots_blocked',
            'home_team_corner_kicks', 'away_team_corner_kicks', 'home_team_offsides',
            'away_team_offsides', 'home_team_fouls', 'away_team_fouls',
            'home_team_throw_ins', 'away_team_throw_ins', 'home_team_yellow_cards',
            'away_team_yellow_cards', 'home_team_red_cards', 'away_team_red_cards',
        )}),
    )
    readonly_fields = []


class MatchEventAdmin(admin.ModelAdmin):
    """Define the admin pages for MatchEvents."""
    ordering = ['event_id']
    list_display = ['event_type', 'player', 'minute', 'match']
    fieldsets = (
        (_('Details'), {'fields': (
            'event_type', 'match', 'player', 'minute', 'second',
            'is_extra_time', 'pitch_area', 'associated_player',
        )}),
    )
    readonly_fields = []


class EventTypeAdmin(admin.ModelAdmin):
    """Define the admin pages for EventTypes."""
    ordering = ['event_type_id']
    list_display = ['event_name']
    fieldsets = (
        (_('Details'), {'fields': ('event_name',)}),
    )
    readonly_fields = []


class PitchLocationAdmin(admin.ModelAdmin):
    """Define the admin pages for PitchLocations."""
    ordering = ['pitch_area_id']
    list_display = ['pitch_area_name']
    fieldsets = (
        (_('Details'), {'fields': ('pitch_area_name',)}),
    )
    readonly_fields = []


class MatchStatusAdmin(admin.ModelAdmin):
    """Define the admin pages for PitchLocations."""
    ordering = ['match_status_id']
    list_display = ['status_name']
    fieldsets = (
        (_('Details'), {'fields': ('status_name',)}),
    )
    readonly_fields = []


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Continent, ContinentAdmin)
admin.site.register(models.Nation, NationAdmin)
admin.site.register(models.City, CityAdmin)
admin.site.register(models.Stadium, StadiumAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Manager, ManagerAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.PlayerRole, PlayerRoleAdmin)
admin.site.register(models.Referee, RefereeAdmin)
admin.site.register(models.Season, SeasonAdmin)
admin.site.register(models.League, LeagueAdmin)
admin.site.register(models.LeagueTable, LeagueTableAdmin)
admin.site.register(models.Fixture, FixtureAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.MatchEvent, MatchEventAdmin)
admin.site.register(models.EventType, EventTypeAdmin)
admin.site.register(models.PitchLocation, PitchLocationAdmin)
admin.site.register(models.MatchStatus, MatchStatusAdmin)
