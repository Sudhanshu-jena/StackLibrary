from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import *
from .email_handler import send_verification_email


def new_project(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'users/project_creator/create_project.html', context)
        else:
            return render(request, 'users/project_creator/create_project.html', context)
    else:
        form = ProjectRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'users/project_creator/create_project.html', context)


def detail_view(request, slug):
    context = {}

    context["task"] = Task.objects.all()
    context["data"] = Project.objects.get(slug=slug)

    return render(request, "users/project_creator/detail_view.html", context)


def update_view(request, id):
    context = {}

    obj = get_object_or_404(Project, id=id)
    form = ProjectUpdateForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/" + "project_creator")

    context["form"] = form

    return render(request, "users/project_creator/update_view.html", context)


def delete_project_view(request, id):
    context = {}

    obj = get_object_or_404(Project, id=id)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/"+ "project_creator")

    return render(request, "users/project_creator/delete_project_view.html", context)


def delete_task_view(request, id):

    context = {}

    obj = get_object_or_404(Task, id=id)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/"+ "project_creator")

    return render(request, "users/project_creator/delete_task_view.html", context)


def update_task_view(request, id):
    context = {}

    obj = get_object_or_404(Task, id=id)

    form = TaskUpdateForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/" + str(6521456588551) + str(id) + str(786498490567823647467849) + '/update')

    context["form"] = form

    return render(request, "users/project_creator/view_update_task.html", context)


def project_creator_login(request):
    obj = Project.objects.all()
    context = {'obj': obj}

    return render(request, "users/project_creator/home.html", context)


def project_creator_add_task(request):
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = TaskRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'users/project_creator/add_task.html', context)
        else:
            return render(request, 'users/project_creator/add_task.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'users/project_creator/add_task.html', context)


def project_creator_register(request):
    if request.method == 'POST':
        form = ProjectCreatorRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect('login')
    else:
        form = ProjectCreatorRegisterForm()
    return render(request, 'users/project_creator_register.html', {'form': form, 'title': 'reqister here'})


@login_required
def project_creator_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProjectCreatorProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.projectcreator)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('project_creator_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProjectCreatorProfileUpdateForm(instance=request.user.projectcreator)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)