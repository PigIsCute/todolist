from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from tasks.models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'todolist.html'
    context_object_name = 'tasks'

class TaskCreateView(CreateView):
    model = Task
    template_name = 'add_task.html'
    fields = ['content', 'status']
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'edit_task.html'
    fields = ['content', 'status']
    success_url = reverse_lazy('task-list') 

class TaskDeleteView(DeleteView):
    model = Task    
    template_name = 'delete_confirm.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('task-list')