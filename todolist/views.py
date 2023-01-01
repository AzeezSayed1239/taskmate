from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist.models import Tasklist
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer = request.user
            instance.save()
        messages.success(request, ("New Task Added!!!"))
        return redirect("todolist")
    else:
        all_tasks = Tasklist.objects.filter(customer=request.user)
        paginator = Paginator(all_tasks, 6)
        page = request.GET.get("pg")
        all_tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {"all_tasks": all_tasks})


@login_required
def delete_task(request, task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.customer == request.user:
        task.delete()
    else:
        messages.error(request, ("Access Restricted!!"))
    return redirect("todolist")


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task_obj = Tasklist.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task_obj)
        if form.is_valid():
            form.save()

        messages.success(request, ("Task Edited!!!"))
        return redirect("todolist")
    else:
        task_obj = Tasklist.objects.get(pk=task_id)
        return render(request, 'edit.html', {"task_obj": task_obj})


@login_required
def complete_task(request, task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.customer == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access Restricted!!"))
    return redirect("todolist")


@login_required
def pending_task(request, task_id):
    task = Tasklist.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect("todolist")


def index(request):
    context = {"index_text": "Welcome on Index Page"}
    return render(request, 'index.html', context)


def aboutus(request):
    context = {"about_text": "Welcome on the About us"}
    return render(request, 'aboutus.html', context)


def contactus(request):
    context = {"contact_text": "Welcome on the Contact Us"}
    return render(request, 'contactus.html', context)
