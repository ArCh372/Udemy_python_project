from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from. forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#Add and editing tasks
@login_required
def todolist(request):     
    if request.method == 'POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            new_form=form.save(commit=False)
            new_form.user=request.user
            new_form.save()
            messages.success(request,"New Task Added!")
            return redirect ('todolist')       
    else:
        task=Task.objects.filter(user=request.user)
        return render(request, 'todo.html', {'all_tasks':task})

@login_required
def edit(request,task_id):
    task=Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form=TaskForm(request.POST,instance = task)
        if form.is_valid():
            form.save()
            messages.success(request,"Task Edited!")
            return redirect ('todolist')
    else:
        return render(request, 'edit.html', {'task_obj':task})

def about(request):
    context={'context':'Welcome to About Task'}
    return render(request,'about.html',context)

def index(request):
    context={'context':'Welcome to Index Task'}
    return render(request,'index.html',context) 

def contact(request):
    context={'context':'Welcome to Contact Task'}
    return render(request,'contact.html',context)

def delete(request,task_id):
    task=Task.objects.get(pk=task_id)
    task.delete()
    return redirect ('todolist')
 
# Complete and pennding tasks
def complete(request,task_id):
    task=Task.objects.get(pk=task_id)
    if task.user == request.user:
        task.done=True
        task.save()
    else:
        messages.error(request,'Access Restricted')
    return redirect ('todolist')
        
def pending(request,task_id):
    task=Task.objects.get(pk=task_id)
    if task.user == request.user:
        task.done=False
        task.save()
    else:
        messages.error(request,'Access Restricted')
    return redirect ('todolist')

