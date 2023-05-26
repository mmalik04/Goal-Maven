"""
Views for the fixture APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from goal_maven.core.models import Season, Fixture, Match
from goal_maven.fixture import serializers
from django.core.exceptions import PermissionDenied
# from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import generics

from django.utils.translation import gettext_lazy as _

# import pdb


class BaseView(viewsets.ModelViewSet):
    """BaseView containing common fields and methods."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Retrieve Leagues/league tables for requested season."""
    #     return self.queryset.filter(season=self.get_season())

    def partial_update(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().update(request, *args, **kwargs)

    def validate_staff(self, request):
        """Validates if user is staff to make modification request."""
        if not request.user.is_staff:
            raise PermissionDenied(
                _("You don't have permission to perform this action.")
            )


class FixtureViewSet(BaseView):
    """View for manage Fixture APIs."""
    serializer_class = serializers.FixtureDetailSerializer
    queryset = Fixture.objects.all()

    def list(self, request, *args, **kwargs):
        """Retrieve Fixture for requested season."""
        season = Season.objects.get(
            season_name=self.kwargs.get('season_name'),
        )
        queryset = self.get_queryset().filter(season=season)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create a new Fixture object."""
        self.validate_staff(request)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Create a new object."""
        serializer.save()
        match_serializer = serializers.MatchSerializer(
            data={'fixture': serializer.instance.fixture_id}
        )
        match_serializer.is_valid(raise_exception=True)
        match_serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Delete a Fixture object."""
        self.validate_staff(request)
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.FixtureSerializer

        return self.serializer_class


class MatchViewSet(BaseView):
    """View for manage Match APIs."""
    serializer_class = serializers.MatchDetailSerializer
    queryset = Match.objects.all()

    def list(self, request, *args, **kwargs):
        """Retrieve Matches for requested season."""
        season = Season.objects.get(
            season_name=self.kwargs.get('season_name'),
        )
        queryset = self.get_queryset().filter(fixture__season=season)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Match object cannot be created directly."""
        raise PermissionDenied('Match object cannot be created directly.')

    def destroy(self, request, *args, **kwargs):
        """Match object cannot be deleted directly."""
        raise PermissionDenied('Match object cannot be deleted directly.')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.MatchSerializer

        return self.serializer_class
