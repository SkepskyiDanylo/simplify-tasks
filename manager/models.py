from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

phone_number_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'",
)


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/default.jpg",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        blank=True,
        null=True,
    )
    information = models.TextField(blank=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_number_validator]
    )
    last_activity = models.DateField(default=timezone.now)

    class Meta:
        ordering = ("position", "username")

    def is_online(self, days: int = 1) -> bool:
        return timezone.now().date() - self.last_activity < timedelta(days=days)

    def __str__(self):
        return f"{self.username}"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=255)
    workers = models.ManyToManyField(Worker, related_name="teams")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="projects")

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
        Project, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True
    )
    tags = models.ManyToManyField(Tag, related_name="tasks")

    class Meta:
        ordering = ("deadline", "priority", "name")

    def __str__(self):
        return f"{self.name}"
