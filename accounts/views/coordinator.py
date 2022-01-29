from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from ..forms import *
from .email_handler import send_verification_email


def view_enroll_details(request, id):
    team = Team.objects.all()
    obj = Enroll.objects.get(id=id)
    context = {'obj': obj, 'team': team}

    return render(request, "users/coordinator/view_all_details.html", context)


def coordinator_login(request):
    obj = Project.objects.all()
    context = {'obj': obj}

    return render(request, "users/coordinator/home.html", context)


def coordinator_detail_view(request, slug):
    team = Team.objects.all()
    data = Project.objects.get(slug=slug)
    task = Task.objects.all()
    enroll = Enroll.objects.all()
    status = Status.objects.all()
    labels = []
    datax = []
    labels1 = []
    datax1 = []
    for y in task:
        if y.project_id == data.id:
            labels.append(y.task_name)

            datax.append(y.Duration.days)
            for z in status:
                if z.task_id == y.id:
                    if z.status == 'Done':
                        labels1.append(y.task_name)

                        datax1.append(y.task_percentage)
        percentage = sum(datax1)

    context = {
        'enroll': enroll,
        'data': data,
        'task': task,
        'team': team,
        'labels':labels,
        'datax': datax,
        'labels1': labels1,
        'datax1': datax1,
        'percentage':percentage,

    }
    return render(request, "users/coordinator/detail_view.html", context)


def coordinator_progress_view(request, id):
    task = Task.objects.get(id=id)
    enroll = Enroll.objects.all()
    comment = TaskComment.objects.all()
    labels1 =[]
    data = []
    labels = []

    for x in enroll:
        if x.project_id == task.project_id:
            if task.status_set.count() == 0:
                    Status.objects.create(status='Yet to start', enrolled_to_id=x.id, task_id=task.id, today=now())
            if task.status_set.count() == 1:
                status_id = Status.objects.get(task_id=task.id)
                obj = get_object_or_404(Status, id=status_id.id)
                status = Status(id=obj.id, enrolled_to=obj.enrolled_to, task_start_date=obj.task_start_date,
                                task_end_date=obj.task_end_date,
                                status=obj.status, submission_file=obj.submission_file, task=task,
                                today=now(), submission=obj.submission)
                status.save()
    for y in comment:
        if y.task_id == task.id:
            labels1.append(y.user.username)

    for z in labels1:
        if z not in labels:
            labels.append(z)

    def countx(labels1, x):
        return labels1.count(x)

    for u in labels:
        data.append(countx(labels1, u))

    context = {
        'enroll': enroll,
        'task': task,
        'labels1': labels1,
        'labels': labels,
        'data': data,
    }

    return render(request, "users/coordinator/progress_view.html", context)


def coordinator_assigned_project(request):
    enroll = Enroll.objects.all()
    obj = Project.objects.all()
    context = {'obj': obj, 'enroll': enroll}

    return render(request, "users/coordinator/assigned_project.html", context)


def coordinator_enroll_project(request, id):
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        task = Task.objects.all()
        requested = RequestedProject.objects.get(id=id)
        context = {'form': form, 'requested': requested}
        if form.is_valid():
            form.save()
            created = True
            form = EnrollForm()
            requested = RequestedProject.objects.get(id=id)
            context = {
                'created': created,
                'form': form,
                'requested': requested,
            }

            return render(request, 'users/coordinator/coordinator_enroll_project.html', context)
        else:
            return render(request, 'users/coordinator/coordinator_enroll_project.html', context)
    else:
        form = EnrollForm()
        requested = RequestedProject.objects.get(id=id)
        context = {
            'form': form,
            'requested': requested,

        }
        return render(request, 'users/coordinator/coordinator_enroll_project.html', context)


def coordinator_edit_project(request):
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        task = Task.objects.all()
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = EnrollForm()

            context = {
                'created': created,
                'form': form,
            }

            return render(request, 'users/coordinator/edit_project.html', context)
        else:
            return render(request, 'users/coordinator/edit_project.html', context)
    else:
        form = EnrollForm()
        context = {
            'form': form,
        }
        return render(request, 'users/coordinator/edit_project.html', context)


def update_enroll_view(request, id):
    context = {}

    obj = get_object_or_404(Enroll, id=id)
    form = EnrollUpdateForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/" + str(id) + '/update_enroll_view')

    context["form"] = form

    return render(request, "users/coordinator/update_enroll_view.html", context)


def coordinator_requested_project(request):
    obj = RequestedProject.objects.all()
    context ={
        'obj':obj,
    }
    return render(request, 'users/coordinator/requested_project.html', context)


def coordinator_register(request):
    if request.method == 'POST':
        form = CoordinatorRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect('login')
    else:
        form = CoordinatorRegisterForm()
    return render(request, 'users/coordinator_register.html', {'form': form, 'title': 'reqister here'})


@login_required
def coordinator_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = CoordinatorProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.coordinator)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('coordinator_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = CoordinatorProfileUpdateForm(instance=request.user.coordinator)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)