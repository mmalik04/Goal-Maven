"""
Serializers for league APIs
"""
from rest_framework import serializers

from goal_maven.core.models import League, Season, LeagueTable
# from goal_maven.core import models

# import pdb


class LeagueSerializer(serializers.ModelSerializer):
    """Serializer for Leagues."""

    class Meta:
        model = League
        fields = ['league_id', 'league_name', 'nation', 'season', 'champion_team',
                  'is_concluded']
        # read_only_fields = ['id']


class LeagueDetailSerializer(LeagueSerializer):
    """Serializer for League detail view."""

    class Meta(LeagueSerializer.Meta):
        fields = LeagueSerializer.Meta.fields + [
            'total_teams',
            'match_day',
            'top_scorer',
            'most_assists',
            'runner_up_team',
        ]


class LeagueTableSerializer(serializers.ModelSerializer):
    """Serializer for League tables"""

    class Meta():
        model = LeagueTable
        fields = ['table_id', 'league', 'season', 'team', 'position', 'points']


class LeagueTableDetailSerializer(LeagueTableSerializer):
    """Serializer for League tables"""

    class Meta(LeagueTableSerializer.Meta):
        fields = LeagueTableSerializer.Meta.fields + ['matches_played', 'matches_won',
                                                      'matches_drawn', 'matches_lost',
                                                      'goals_scored', 'goals_against',
                                                      'goal_difference']


class SeasonSerializer(serializers.ModelSerializer):
    """Serializer for Seasons."""

    class Meta:
        model = Season
        fields = ['season_id', 'season_name', 'is_concluded', 'top_scorer']


class SeasonDetailSerializer(SeasonSerializer):
    """Serializer for Season detail view."""

    class Meta(SeasonSerializer.Meta):
        fields = SeasonSerializer.Meta.fields + [
            'start_date',
            'end_date',
            'number_of_leagues',
            'number_of_matches',
            'goals_scored',
            'avg_goals_per_match',
        ]
