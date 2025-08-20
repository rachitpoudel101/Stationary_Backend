from django.core.management.base import BaseCommand
from core.apps.users.models import Users

print("create_admin command module loaded")


class Command(BaseCommand):
    help = "Create an initial admin user"

    def handle(self, *args, **kwargs):
        admin_email = "superuser@superuser.com"
        admin_password = "superuser"
        admin_username = "superuser"

        if not Users.objects.filter(username=admin_username).exists():
            Users.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                is_super=True,
                role="admin",
            )
            self.stdout.write(self.style.SUCCESS("Admin user created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists"))
