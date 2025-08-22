from rest_framework import serializers
from core.apps.users.models import Users

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Users
        fields = [
            "id",
            "first_name",
            "last_name",
            'password',
            "username",
            "role",
            "email",

        ]
    def validate(self, data):
        username = data.get('username')
        if Users.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        
        return data

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data["username"],
            role=validated_data["role"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        user.set_password(validated_data.get("password"))
        user.is_staff = True
        user.save()
        return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)