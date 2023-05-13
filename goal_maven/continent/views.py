"""
Views for the continent APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from goal_maven.core.models import Continent
from goal_maven.continent import serializers


class ContinentViewSet(viewsets.ModelViewSet):
    """View for manage continent APIs."""
    serializer_class = serializers.ContinentDetailSerializer
    queryset = Continent.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ContinentSerializer

        return self.serializer_class

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, self.request.user, *args, **kwargs)
