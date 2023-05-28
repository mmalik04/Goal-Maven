"""
Serializers for team APIs
"""
from rest_framework import serializers

from goal_maven.core.models import Team
from goal_maven.core import models
from django.db.models import Count

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
    most_goals = serializers.SerializerMethodField()
    most_assists = serializers.SerializerMethodField()
    most_yellow_cards = serializers.SerializerMethodField()
    most_red_cards = serializers.SerializerMethodField()

    def get_season(self, team) -> str:
        """get the season for stats"""
        return self.context.get('season_name')

    def stat(self, team, season_name) -> type(models.LeagueTable):
        """Get stats for a team in a season."""
        return models.LeagueTable.objects.get(
            team=team,
            season__season_name=season_name,
        )

    def get_points(self, team) -> int:
        """Get points for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.points

    def get_position(self, team) -> int:
        """Get position for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.position

    def get_matches_played(self, team) -> int:
        """Get matches played for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.matches_played

    def get_matches_won(self, team) -> int:
        """Get matches won for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.matches_won

    def get_matches_drawn(self, team) -> int:
        """Get matches drawn for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.matches_drawn

    def get_matches_lost(self, team) -> int:
        """Get matches lost for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.matches_lost

    def get_goals_scored(self, team) -> int:
        """Get goals scored for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.goals_scored

    def get_goals_against(self, team) -> int:
        """Get goals against for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.goals_against

    def get_goal_difference(self, team) -> int:
        """Get goal difference for a team in a season."""
        stat = self.stat(team, self.get_season(team))

        return stat.goal_difference

    def get_most_goals(self, team) -> int:
        """Get player with most goals for a team in a season."""
        goal_scorers = models.MatchEvent.objects.filter(
            match__fixture__season__season_name=self.get_season(team),
            event_type__event_name__in=['Goal', 'Penalty Goal', 'Free Kick Goal'],
            player__team=team,
        ).values('player__player_name').annotate(
            total_goals=Count('player__player_name')
        ).order_by('-total_goals')

        if goal_scorers:
            return goal_scorers[0]
        return None

    def get_most_assists(self, team) -> int:
        """Get player with most assists for a team in a season."""
        assisting_players = models.MatchEvent.objects.filter(
            match__fixture__season__season_name=self.get_season(team),
            event_type__event_name='Goal',
            associated_player__team=team,
        ).values('associated_player__player_name').annotate(
            total_assists=Count('associated_player__player_name')
        ).order_by('-total_assists')

        if assisting_players:
            return assisting_players[0]
        return None

    def get_most_yellow_cards(self, team) -> int:
        """Get player with most yellow cards for a team in a season."""
        yellow_card_players = models.MatchEvent.objects.filter(
            match__fixture__season__season_name=self.get_season(team),
            event_type__event_name='Yellow Card',
            player__team=team,
        ).values('player__player_name').annotate(
            total_yellow_cards=Count('player__player_name')
        ).order_by('-total_yellow_cards')

        if yellow_card_players:
            return yellow_card_players[0]
        return None

    def get_most_red_cards(self, team) -> int:
        """Get player with most red cards for a team in a season."""
        red_card_players = models.MatchEvent.objects.filter(
            match__fixture__season__season_name=self.get_season(team),
            event_type__event_name='Red Card',
            player__team=team,
        ).values('player__player_name').annotate(
            total_red_cards=Count('player__player_name')
        ).order_by('-total_red_cards')

        if red_card_players:
            return red_card_players[0]
        return None

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['season', 'points', 'position',
                                               'matches_played', 'matches_won',
                                               'matches_drawn', 'matches_lost',
                                               'goals_scored', 'goals_against',
                                               'goal_difference', 'most_goals',
                                               'most_assists', 'most_yellow_cards',
                                               'most_red_cards']
