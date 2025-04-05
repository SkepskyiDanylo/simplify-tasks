import os
import uuid
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


phone_number_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'",
)


def unique_file_path(instance: callable, filename: str) -> str:
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("profile_pictures/", filename)


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    profile_picture = models.ImageField(
        upload_to=unique_file_path,
        default="profile_pictures/default.jpg",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="workers",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_number_validator]
    )
    last_activity = models.DateField(default=timezone.now)
    is_online = models.BooleanField(default=False)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey(
        "Team",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="workers"
    )

    class Meta:
        ordering = ("position", "username")

    def __str__(self):
        return f"{self.username}"

    def check_is_online(self, days: int = 1) -> bool:
        status = (timezone.now().date()
                  - self.last_activity < timedelta(days=days))
        self.is_online = status
        self.save()
        return status

    def reset_picture(self) -> None:
        if self.profile_picture.name != self.profile_picture.field.default:
            self.profile_picture.delete(save=False)
        self.profile_picture = self.profile_picture.field.default
        self.save()


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=255)
    leader = models.ForeignKey(
        "Worker",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="leader_of"
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )

    def __str__(self):
        return f"{self.name}, (Team: {self.team})"


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    choices = [
        (1, "Lowest"),
        (2, "Low"),
        (3, "Medium"),
        (4, "High"),
        (5, "Highest"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=choices, default=3)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assigners = models.ManyToManyField(Worker, related_name="tasks")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(Tag, related_name="tasks")
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("deadline", "priority", "name")

    def __str__(self):
        return f"{self.name}"
