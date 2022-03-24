from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import *
from .email_handler import send_verification_email


def hod_login(request):
    obj = Project.objects.all()
    obj1 = Project.objects.filter(batch=11)
    obj2 = Project.objects.filter(batch=6)
    obj3 = Project.objects.filter(batch=5)
    obj4 = Project.objects.filter(batch=4)
    context = {'obj': obj,
               'obj1': obj1,
               'obj2': obj2,
               'obj3': obj3,
               'obj4': obj4,
               }

    return render(request, "users/hod/home.html", context)


def hod_detail_view(request, slug):
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
        'labels': labels,
        'datax': datax,
        'labels1': labels1,
        'datax1': datax1,
        'percentage': percentage,

    }
    return render(request, "users/hod/detail_view.html", context)


def hod_enroll_details(request, id):
    team = Team.objects.all()
    obj = Enroll.objects.get(id=id)
    interaction = TaskComment.objects.all()
    labels1 = []
    labels = []
    data = []
    for guide in obj.guide_or_industry_mentor.all():
        labels.append(guide.username)
    for y in team:
        if y.id == obj.team_id:
            for x in y.members.all():
                labels.append(x.username)

    def countx(labels1, x):
        return labels1.count(x)

    for u in labels:
        for x in interaction:
            if u == x.user.username:
                labels1.append(u)
    for c in labels:
        data.append(countx(labels1, c))
    context = {
        'obj': obj,
        'team': team,
        'labels': labels,
        'labels1':labels1,
        'data': data,
    }

    return render(request, "users/hod/hod_enroll_details.html", context)


def hod_register(request):
    if request.method == 'POST':
        form = HodRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect('login')
    else:
        form = HodRegisterForm()
    return render(request, 'users/hod_register.html', {'form': form, 'title': 'reqister here'})


@login_required
def hod_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = HodProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.hod)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('hod_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = HodProfileUpdateForm(instance=request.user.hod)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)