from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, redirect_to_login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task, Project


class UserLoginView(LoginView):
    template_name = "todo/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("projects")


class UserRegistrationView(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("projects")
    template_name = "todo/register.html"

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegistrationView, self).form_valid(form)

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            return redirect("projects")
        return super(UserRegistrationView, self).get(*args, **kwargs)


class ProjectsListView(ListView):
    model = Project
    template_name = "todo/projects_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.filter(user=self.request.user)
        context["projects"] = projects
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["title"]
    success_url = reverse_lazy("projects")
    template_name = "todo/project_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreateView, self).form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ["title"]
    success_url = reverse_lazy("projects")
    template_name = "todo/project_update.html"


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    context_object_name = "project"
    template_name = "todo/project_delete.html"
    success_url = reverse_lazy("projects")


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo/tasks.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project_id = self.kwargs.get("project_id")
        context["tasks"] = context["tasks"].filter(project__id=project_id)

        context["project"] = Project.objects.get(pk=project_id)

        sort_by = self.request.GET.get("sort_by", "")
        if sort_by == "completion":
            completed_tasks = context["tasks"].filter(is_done=True)
            uncompleted_tasks = context["tasks"].filter(is_done=False)
            context["tasks"] = completed_tasks | uncompleted_tasks
        if sort_by == "priority":
            low_prior_tasks = context["tasks"].filter(priority_level="low")
            medium_prior_tasks = context["tasks"].filter(priority_level="medium")
            high_prior_tasks = context["tasks"].filter(priority_level="high")
            context["tasks"] = high_prior_tasks | medium_prior_tasks | low_prior_tasks

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "todo/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "content", "is_done", "deadline", "priority_level"]
    template_name = "todo/task_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        project_id = self.kwargs.get("project_id")
        form.instance.project = Project.objects.get(pk=project_id)
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        project_id = self.kwargs.get("project_id")
        return reverse_lazy("tasks", kwargs={"project_id": project_id})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "content", "is_done", "deadline", "priority_level"]
    template_name = "todo/task_update.html"

    def get_success_url(self) -> str:
        project_id = self.get_object().project.id
        context = {"project_id": project_id}
        return reverse_lazy("tasks", kwargs=context)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "todo/task_delete.html"

    def get_success_url(self) -> str:
        project_id = self.get_object().project.id
        context = {"project_id": project_id}
        return reverse_lazy("tasks", kwargs=context)
