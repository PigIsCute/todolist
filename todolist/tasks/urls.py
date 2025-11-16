from django.urls import path
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('list/', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:task_id>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:task_id>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]

