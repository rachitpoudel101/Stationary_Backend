from django.urls import path

from core.apps.dashboard.views import dashboard_stats

urlpatterns = [
    path("stats/", dashboard_stats, name="dashboard-stats"),
]
