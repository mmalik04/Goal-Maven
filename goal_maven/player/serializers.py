"""
Serializers for player APIs
"""
from rest_framework import serializers

from goal_maven.core.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for players."""

    class Meta:
        model = Player
        fields = ['player_name', 'jersy_number', 'team', 'nation', 'role']
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


# class ContinentSerializer(serializers.ModelSerializer):
#     """Serializer for continents."""

#     class Meta:
#         model = Continent
#         fields = ['continent_name']
#         # read_only_fields = ['id']

# class ContinentDetailSerializer(ContinentSerializer):
#     """Serializer for continent detail view."""

#     class Meta(ContinentSerializer.Meta):
#         fields = ContinentSerializer.Meta.fields + ['continent_id']
