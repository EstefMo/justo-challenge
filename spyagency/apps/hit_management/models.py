from django.contrib.auth.models import User
from django.db import models


class Hitman(models.Model):
    HITMAN_STATUS = (("ACTIVE", "Active"), ("INACTIVE", "Inactive"))

    user = models.OneToOneField(User, related_name="userId", on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    status = models.CharField(max_length=8, choices=HITMAN_STATUS, default="ACTIVE")


class Hit(models.Model):
    HIT_STATUS = (
        ("OPENED", "opened"),
        ("ASSIGNED", "assigned"),
        ("COMPLETED", "completed"),
        ("FAILED", "failed"),
    )
    assignee = models.ForeignKey(
        "Hitman",
        related_name="assignee",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    creator = models.ForeignKey(
        "Hitman", related_name="creator", on_delete=models.CASCADE
    )
    target_name = models.CharField(max_length=45)
    status = models.CharField(max_length=15, choices=HIT_STATUS)
    description = models.CharField(max_length=150, default=None)


class Manager(models.Model):
    user = models.OneToOneField(Hitman, on_delete=models.CASCADE, primary_key=True)
    lackeys = models.ManyToManyField(Hitman, related_name="managers", blank=True)

    def __str__(self):
        return self.user.user.first_name
