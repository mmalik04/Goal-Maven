"""
Serializers for player APIs
"""
from rest_framework import serializers

from goal_maven.core.models import Player
from goal_maven.core import models

# import pdb


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for players."""

    class Meta:
        model = Player
        fields = ['player_id', 'player_name', 'jersy_number', 'team', 'nation', 'role']
        # read_only_fields = ['id']


class PlayerDetailSerializer(PlayerSerializer):
    """Serializer for player detail view."""

    class Meta(PlayerSerializer.Meta):
        fields = PlayerSerializer.Meta.fields + [
            'date_of_birth',
            'career_start',
            'height',
            'weight',
            'total_appearances',
        ]


class PlayerStatsSerializer(serializers.Serializer):
    """Serializer for player goal view."""

    season = serializers.SerializerMethodField()
    goals = serializers.SerializerMethodField()
    assists = serializers.SerializerMethodField()
    fouls = serializers.SerializerMethodField()
    yellow_cards = serializers.SerializerMethodField()
    red_cards = serializers.SerializerMethodField()
    shots_on = serializers.SerializerMethodField()
    own_goals = serializers.SerializerMethodField()

    def get_season(self, player) -> str:
        """get the season for stats"""
        return self.context.get('season_name')

    def get_goals(self, player) -> int:
        goals = models.MatchEvent.objects.filter(
            player=player,
            match__fixture__season__season_name=self.get_season(player),
            event_type__event_name__in=['Goal', 'Penalty Goal', 'Free Kick Goal'],
        )

        return goals.count()

    def get_assists(self, player) -> int:
        assists = models.MatchEvent.objects.filter(
            associated_player=player,
            event_type__event_name='Goal',
        )

        return assists.count()

    def get_fouls(self, player) -> int:
        fouls = models.MatchEvent.objects.filter(
            player=player,
            event_type__event_name__in=['Foul', 'Penalty Foul'],
        )

        return fouls.count()

    def get_yellow_cards(self, player) -> int:
        yellow_cards = models.MatchEvent.objects.filter(
            player=player,
            event_type__event_name='Yellow Card',
        )

        return yellow_cards.count()

    def get_red_cards(self, player) -> int:
        red_cards = models.MatchEvent.objects.filter(
            player=player,
            event_type__event_name='Red Card',
        )

        return red_cards.count()

    def get_shots_on(self, player) -> int:
        shots_on = models.MatchEvent.objects.filter(
            player=player,
            event_type__event_name='Shot On',
        )

        return shots_on.count()

    def get_own_goals(self, player) -> int:
        own_goals = models.MatchEvent.objects.filter(
            player=player,
            event_type__event_name='Own Goal',
        )

        return own_goals.count()

    class Meta(PlayerSerializer.Meta):
        fields = ['player_id', 'player_name', 'team', 'season', 'goals', 'assists',
                  'fouls', 'yellow_cards', 'red_cards', 'shots_on', 'own_goals']
