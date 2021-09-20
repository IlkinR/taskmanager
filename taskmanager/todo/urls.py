from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Auth
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    # Project
    path("projects/", views.ProjectsListView.as_view(), name="projects"),
    path("project_new/", views.ProjectCreateView.as_view(), name="project_create"),
    path(
        "project_update/<int:pk>/",
        views.ProjectUpdateView.as_view(),
        name="project_update",
    ),
    path(
        "project_delete/<int:pk>/",
        views.ProjectDeleteView.as_view(),
        name="project_delete",
    ),
    # Tasks
    path("project<int:project_id>/tasks", views.TasksListView.as_view(), name="tasks"),
    path("task_<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("task_new/<int:project_id>/", views.TaskCreateView.as_view(), name="task_create"),
    path("task_update/<int:pk>/", views.TaskUpdateView.as_view(), name="task_update"),
    path("task_delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task_delete"),
]
