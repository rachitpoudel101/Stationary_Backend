from django.urls import path

from core.apps.Supliers.views import SupliersDetailView, SupliersListCreateView

urlpatterns = [
    path("supliers/", SupliersListCreateView.as_view(), name="supliers-list-create"),
    path("supliers/<int:id>/", SupliersDetailView.as_view(), name="supliers-detail"),
]
