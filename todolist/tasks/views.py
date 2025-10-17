from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.models import Task

# Create your views here.
def list_tasks(request):
    tasks = Task.objects.all()
    return render(request, "todolist.html", locals())

def add_task(request):
    if request.method == 'GET':
        return render(request, "add_task.html", locals())
    elif request.method == 'POST':
        content = request.POST['content']
        Task.objects.create(content=content, status='undo')
        return redirect('list_tasks')

def edit_task(request, task_id):
    if request.method == 'GET':
        return render(request, "edit_task.html", locals())
    elif request.method == 'POST':
        content = request.POST['content']
        status = request.POST['status']
        task = Task.objects.get(id=task_id)
        task.content = content
        task.status = status
        task.save()
        return redirect('list_tasks')

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('list_tasks')