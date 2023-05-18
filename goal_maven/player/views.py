"""
Views for the player APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from goal_maven.core.models import Player
from goal_maven.player import serializers
from django.core.exceptions import PermissionDenied

from django.utils.translation import gettext_lazy as _

# import pdb


class PlayerViewSet(viewsets.ModelViewSet):
    """View for manage player APIs."""
    serializer_class = serializers.PlayerDetailSerializer
    queryset = Player.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Retrieve players for authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PlayerSerializer

        return self.serializer_class

    def validate_staff(self, request):
        """Validates if user is staff to make modification request."""
        if not request.user.is_staff:
            raise PermissionDenied(
                _("You don't have permission to perform this action.")
            )
