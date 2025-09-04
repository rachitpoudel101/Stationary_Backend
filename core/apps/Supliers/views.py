from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.Supliers.models import Supliers
from core.apps.Supliers.serializers import SupliersCreateSerializer, SupliersSerializer
from core.apps.users.permissions.permissions import IsAdmin, IsSuperAdmin


class SupliersListCreateView(generics.ListCreateAPIView):
    queryset = Supliers.objects.filter(is_deleted=False)
    serializer_class = SupliersCreateSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SupliersCreateSerializer
        return SupliersSerializer


class SupliersDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsSuperAdmin]
    queryset = Supliers.objects.filter(is_deleted=False)
    serializer_class = SupliersCreateSerializer
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
