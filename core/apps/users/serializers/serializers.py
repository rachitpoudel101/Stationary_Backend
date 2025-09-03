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
            "password",
            "username",
            "role",
            "email",
        ]

    def validate(self, data):
        username = data.get("username")
        if Users.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "This username is already taken."}
            )
        request = self.context.get("request")
        if request:
            creator = request.user
            new_role = data.get("role")
            if new_role == "admin" and not getattr(creator, "is_superuser", False):
                raise serializers.ValidationError(
                    {"role": "Only superadmin can create admin users."}
                )
            if new_role == "staff" and getattr(creator, "role", None) == "admin":
                pass
            elif new_role == "admin" and getattr(creator, "role", None) == "admin":
                raise serializers.ValidationError(
                    {"role": "Admin cannot create another admin."}
                )
            elif (
                new_role == "staff"
                and getattr(creator, "role", None) != "admin"
                and not getattr(creator, "is_superuser", False)
            ):
                raise serializers.ValidationError(
                    {"role": "Only admin or superadmin can create staff users."}
                )
        return data

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data["username"],
            role=validated_data["role"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data.get("password"))
        if user.role == Users.RolesChoices.STAFF:
            user.is_staff = True
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update normal fields
        for attr, value in validated_data.items():
            if attr == "password":
                continue  # handle separately
            setattr(instance, attr, value)

        # Update password properly
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        # Ensure staff flag aligns with role
        if instance.role == Users.RolesChoices.STAFF:
            instance.is_staff = True
        elif instance.role == Users.RolesChoices.ADMIN:
            instance.is_staff = True  # admins are staff too
        else:
            instance.is_staff = False

        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


class SelfAPISerilizer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "role",
        ]
