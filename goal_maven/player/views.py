"""
Views for the player APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from goal_maven.core.models import Player
from goal_maven.player import serializers

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

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PlayerSerializer

        return self.serializer_class

    # def create(self, request, *args, **kwargs):
    #     pdb.set_trace()

    # def perform_create(self, serializer):
    #     """Create a new player."""
    #     # pdb.set_trace()
    #     serializer.save()

# class ContinentViewSet(viewsets.ModelViewSet):
#     """View for manage continent APIs."""
#     serializer_class = serializers.ContinentDetailSerializer
#     queryset = Player.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_serializer_class(self):
#         """Return the serializer class for request."""
#         if self.action == 'list':
#             return serializers.ContinentSerializer

#         return self.serializer_class
