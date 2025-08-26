from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.users.views import LogoutView, UserViewSet, SelfDetails, UserRoleUpdateAPIView, RoleConfigView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("self/", SelfDetails.as_view(),name="self"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("role-update/<int:user_id>/", UserRoleUpdateAPIView.as_view(), name="role-update"),
    path("role-config/", RoleConfigView.as_view(), name="role-config"),
]