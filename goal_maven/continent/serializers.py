"""
Serializers for continent APIs
"""
from rest_framework import serializers

from goal_maven.core.models import Continent


class ContinentSerializer(serializers.ModelSerializer):
    """Serializer for continents."""

    class Meta:
        model = Continent
        fields = ['continent_name']
        # read_only_fields = ['id']


class ContinentDetailSerializer(ContinentSerializer):
    """Serializer for continent detail view."""

    class Meta(ContinentSerializer.Meta):
        fields = ContinentSerializer.Meta.fields + ['continent_id']
