from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Position, TaskType, Task, Team, Project, Worker, Tag

admin.site.unregister(Group)


@admin.register(Worker)
class AuthUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info",
          {"fields": ("position", "profile_picture", "team")}), )
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info",
          {"fields": ("position", "profile_picture", "team")}), )
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "priority", "is_completed")
    list_filter = ("is_completed", "priority", "tags")
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team")
