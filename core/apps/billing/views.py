from rest_framework import viewsets
from core.apps.billing.models import Bill
from core.apps.billing.serializers.serializers import BillSerializer
from core.apps.users.permissions.permissions import IsSuperAdmin, IsAdmin, Isstaff
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsSuperAdmin | IsAdmin | Isstaff]