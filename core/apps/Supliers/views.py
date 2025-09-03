from rest_framework import generics

from core.apps.Supliers.models import Supliers
from core.apps.Supliers.serializers import SupliersCreateSerializer, SupliersSerializer
from core.apps.users.permissions.permissions import IsAdmin, IsSuperAdmin


class SupliersListCreateView(generics.ListCreateAPIView):
    queryset = Supliers.objects.all()
    serializer_class = SupliersCreateSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SupliersCreateSerializer
        return SupliersSerializer


class SupliersDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsSuperAdmin]
    queryset = Supliers.objects.all()
    serializer_class = SupliersCreateSerializer
    lookup_field = "id"
