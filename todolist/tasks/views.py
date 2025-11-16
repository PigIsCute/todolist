from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.urls import reverse_lazy
from tasks.models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin 

# Create your views here.
class TaskListView(ListView, LoginRequiredMixin):
    model = Task
    template_name = 'todolist.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    
class TaskCreateView(CreateView, LoginRequiredMixin):
    model = Task
    template_name = 'add_task.html'
    fields = ['content', 'status']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TaskUpdateView(UpdateView, LoginRequiredMixin):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'edit_task.html'
    fields = ['content', 'status']
    success_url = reverse_lazy('task-list') 
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class TaskDeleteView(DeleteView, LoginRequiredMixin):
    model = Task    
    template_name = 'delete_confirm.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)