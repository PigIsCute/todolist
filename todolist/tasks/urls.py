from django.urls import path
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('tasks/list/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:task_id>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:task_id>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]

