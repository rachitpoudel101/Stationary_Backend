import traceback
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from core.apps.users.permissions.permissions import IsSuperAdmin
from core.apps.users.models import Users
from core.apps.users.serializers.serializers import UserCreateSerializer, LogoutSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsSuperAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class SelfDetails(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreateSerializer

    def list(self, request, *args, **kwargs):
        try:
            user = self.queryset.filter(id=request.user.id).first()
            if not user:
                return Response(
                    {"detail": "User not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(user, context={"request": request})
            data = serializer.data
            data["is_superuser"] = request.user.is_superuser

            return Response(data)
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            try:
                token.blacklist()
                return Response({"detail": "Token blacklisted"}, status=status.HTTP_205_RESET_CONTENT)
            except AttributeError:
                return Response({"detail": "Blacklisting not supported. Check your configuration."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)