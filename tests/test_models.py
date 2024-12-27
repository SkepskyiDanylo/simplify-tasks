from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import (
    Position,
    TaskType,
    Tag,
    Team,
    Project,
    Task
)


class TestModels(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.tag = Tag.objects.create(
            name="Test Tag",
        )
        self.team = Team.objects.create(
            name="Test Team",
        )
        self.worker = get_user_model().objects.create_user(
            username="Test Worker",
            position=self.position,
            password="password",
        )
        self.project = Project.objects.create(
            name="Test Project",
            team=self.team,
        )
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Task",
            deadline=timezone.now(),
            task_type=self.task_type,
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), f"{self.position.name}")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), f"{self.task_type.name}")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), f"{self.tag.name}")

    def test_team_str(self):
        self.assertEqual(str(self.team), f"{self.team.name}")

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.username}, ({self.worker.first_name}, {self.worker.last_name})"
        )

    def test_project_str(self):
        self.assertEqual(
            str(self.project),
            f"{self.project.name}, (Team: {self.project.team.name})"
        )

    def test_task_str(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.name}, (Completed {self.task.is_completed})"
        )