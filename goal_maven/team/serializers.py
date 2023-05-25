"""
Serializers for team APIs
"""
from rest_framework import serializers

from goal_maven.core.models import Team
from goal_maven.core import models

# import pdb


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Teams."""

    class Meta:
        model = Team
        fields = ['team_id', 'team_name', 'league']
        # read_only_fields = ['id']


class TeamDetailSerializer(TeamSerializer):
    """Serializer for Team detail view."""

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + [
            'est_date',
            'stadium',
            'manager',
        ]


class TeamStatsSerializer(serializers.Serializer):
    """Serializer for Team stats view."""

    season = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    matches_played = serializers.SerializerMethodField()
    matches_won = serializers.SerializerMethodField()
    matches_drawn = serializers.SerializerMethodField()
    matches_lost = serializers.SerializerMethodField()
    goals_scored = serializers.SerializerMethodField()
    goals_against = serializers.SerializerMethodField()
    goal_difference = serializers.SerializerMethodField()

    def get_season(self, team) -> str:

        return self.context.get('season_name')

    def stat(self, team, season_name) -> type(models.LeagueTable):
        return models.LeagueTable.objects.get(
            team=team,
            season__season_name=season_name,
        )

    def get_points(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.points

    def get_position(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.position

    def get_matches_played(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.matches_played

    def get_matches_won(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.matches_won

    def get_matches_drawn(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.matches_drawn

    def get_matches_lost(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.matches_lost

    def get_goals_scored(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.goals_scored

    def get_goals_against(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.goals_against

    def get_goal_difference(self, team) -> int:
        stat = self.stat(team, self.get_season(team))

        return stat.goal_difference

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['season', 'points', 'position',
                                               'matches_played', 'matches_won',
                                               'matches_drawn', 'matches_lost',
                                               'goals_scored', 'goals_against',
                                               'goal_difference']
