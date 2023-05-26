"""
Serializers for fixture APIs
"""
from rest_framework import serializers

from goal_maven.core.models import Fixture, Match
# from goal_maven.core import models

# import pdb


class FixtureSerializer(serializers.ModelSerializer):
    """Serializer for Fixtures."""

    class Meta:
        model = Fixture
        fields = ['fixture_id', 'season', 'league', 'date', 'time', 'home_team',
                  'away_team', 'match_day', 'match_status']
        # read_only_fields = ['id']


class FixtureDetailSerializer(FixtureSerializer):
    """Serializer for Fixture detail view."""

    class Meta(FixtureSerializer.Meta):
        fields = FixtureSerializer.Meta.fields + [
            'home_team_manager',
            'away_team_manager',
            'stadium',
            'referee',
        ]


class MatchSerializer(serializers.ModelSerializer):
    """Serializer for Matches."""

    class Meta:
        model = Match
        fields = ['match_id', 'fixture', 'result', 'winner_team']
        # read_only_fields = ['id']


class MatchDetailSerializer(MatchSerializer):
    """Serializer for Match detail view."""

    class Meta(MatchSerializer.Meta):
        fields = MatchSerializer.Meta.fields + [
            'extra_time',
            'injury_time',
            'home_team_goals',
            'away_team_goals',
            'home_team_possession',
            'away_team_possession',
            'home_team_shots',
            'away_team_shots',
            'home_team_shots_on_target',
            'away_team_shots_on_target',
            'home_team_shots_off_target',
            'away_team_shots_off_target',
            'home_team_shots_blocked',
            'away_team_shots_blocked',
            'home_team_corner_kicks',
            'away_team_corner_kicks',
            'home_team_offsides',
            'away_team_offsides',
            'home_team_fouls',
            'away_team_fouls',
            'home_team_throw_ins',
            'away_team_throw_ins',
            'home_team_yellow_cards',
            'away_team_yellow_cards',
            'home_team_red_cards',
            'away_team_red_cards',
        ]
