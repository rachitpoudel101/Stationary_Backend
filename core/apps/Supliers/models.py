from django.db import models


class Supliers(models.Model):
    class Meta:
        db_table = "supliers"

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name
