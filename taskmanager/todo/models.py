from datetime import date
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

PRIORITY_LEVEL = (
    ("low", "LOW"),
    ("medium", "MEDIUM"),
    ("high", "HIGH"),
)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=date.today)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    priority_level = models.CharField(
        max_length=200, choices=PRIORITY_LEVEL, null=True, blank=True, default="low"
    )
    is_done = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def get_absolute_url(self):
        context = {"project_id": self.project.id}
        return reverse_lazy("tasks", kwargs=context)

    def __str__(self):
        return self.title
