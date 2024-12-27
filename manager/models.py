from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="workers", blank=True, null=True)

    class Meta:
        ordering = ("position", "username")

    def __str__(self):
        return f"{self.username}, ({self.first_name}, {self.last_name})"


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
        return f"{self.name} (Team: {self.team})"

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Task(models.Model):
    choices = [
        (1,"Lowest"),
        (2,"Low"),
        (3,"Medium"),
        (4,"High"),
        (5,"Highest"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=choices, default=3)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assigners = models.ManyToManyField(Worker, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="tasks")

    class Meta:
        ordering = ("deadline", "priority", "name")

    def __str__(self):
        return f"{self.name}, (Completed {self.is_completed})"
