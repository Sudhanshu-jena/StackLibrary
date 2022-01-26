from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from ..forms import *
from verify_email.email_handler import send_verification_email


def student_login(request):
    projects = Project.objects.all()
    enrolls = Enroll.objects.all()
    teams = Team.objects.all()

    context = {
        'projects': projects,
        'enrolls' : enrolls,
        'teams' : teams,
    }
    return render(request, 'users/student/home.html', context)


def student_detail_view(request, id):
    team = Team.objects.all()
    data = Project.objects.get(id=id)
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
    return render(request, "users/student/detail_view.html", context)


def view_team(request, id):
    obj = Team.objects.get(id=id)
    context = {'obj': obj}
    return render(request, "users/student/view_team.html", context)


def student_team_view(request):
    enrolls = Enroll.objects.all()
    teams = Team.objects.all()
    context = {
        'teams': teams,
        'enrolls': enrolls,
    }
    return render(request, 'users/student/team_view.html', context)


def student_team_create(request):
    if request.method == 'POST':
        form = StudentTeamForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = StudentTeamForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'users/student/team.html', context)
        else:
            return render(request, 'users/student/team.html', context)
    else:
        form = StudentTeamForm()
        context = {
            'form': form,
        }
        return render(request, 'users/student/team.html', context)


def student_project(request):
    projects = Project.objects.all()
    enrolls = Enroll.objects.all()
    teams = Team.objects.all()

    context = {
        'projects': projects,
        'enrolls': enrolls,
        'teams': teams,
    }
    return render(request, 'users/student/assigned_project.html', context)


def task_comment_student(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = TaskComment(comment=comment, user=user, task=task)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = TaskComment.objects.get(sno=parentSno)
            comment = TaskComment(comment=comment, user=user, task=task, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/task_view/8464648651684118{task.id}4846474141146")


def task_view(request, id):
    task = Task.objects.get(id=id)
    enroll = Enroll.objects.all()
    comments = TaskComment.objects.filter(task=task, parent=None)
    replies = TaskComment.objects.filter(task=task).exclude(parent=None)
    for x in enroll:
        if x.project_id == task.project_id:
            if task.status_set.count() == 0:
                Status.objects.create(status='Yet to start', enrolled_to_id=x.id, task_id=task.id)
            if task.status_set.count() == 1:
                status_id = Status.objects.get(task_id=task.id)
                obj = get_object_or_404(Status, id=status_id.id)
                status = Status(id=obj.id, enrolled_to=obj.enrolled_to, task_start_date=obj.task_start_date,
                                task_end_date=obj.task_end_date,
                                status=obj.status, submission_file=obj.submission_file, task=task,
                                today=now(), submission=obj.submission)
                status.save()
    if request.method == "POST":
        status_id = Status.objects.get(task_id=task.id)
        obj = get_object_or_404(Status, id=status_id.id)
        n = request.FILES['submission_file']
        s = request.POST['submission']
        status = Status(id=obj.id, enrolled_to=obj.enrolled_to, task_start_date=obj.task_start_date, task_end_date=obj.task_end_date,
                        status=obj.status, submission_file=n, task=task, submission=s, today=now())
        status.save()
        return redirect(f"/task_view/8464648651684118{task.id}4846474141146")
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {
        'enroll': enroll,
        'replyDict': replyDict,
        'comments': comments,
        'task': task,
    }
    return render(request, "users/student/task.html", context)


def student_enroll_details(request, id):
    team = Team.objects.all()
    obj = Enroll.objects.get(id=id)
    context = {'obj': obj, 'team': team}

    return render(request, "users/student/view_enroll_details.html", context)


def request_project_confirm(request, id):
    if request.method == 'POST':
        form = RequestProjectForm(request.POST)
        obj = Project.objects.get(id=id)
        context = {'form': form, 'obj': obj,}
        if form.is_valid():
            fm = form.save()
            fm.requested_project_id = obj.id
            fm.save()
            messages.success(request, f"Your request has been submitted successfully for {obj}")

            return render(request, 'users/student/success.html', context)
        else:
            return render(request, 'users/student/confirm_project_request.html', context)
    else:
        form = RequestProjectForm()
        obj = Project.objects.get(id=id)
        context = {
            'form': form,
            'obj': obj,
        }
        return render(request, 'users/student/confirm_project_request.html', context)


def request_project(request):
    enrolls = Enroll.objects.all()
    obj = Project.objects.all()
    projects = []
    remaining = []
    for x in obj:
        remaining.append(x.id)

    for enroll in enrolls:
        projects.append(enroll.project_id)

    for i in projects:
        if i in remaining:
            remaining.remove(i)
    context = {
        'obj': obj,
        'enrolls': enrolls,
        'projects': projects,
        'remaining': remaining,

        }

    return render(request, "users/student/all_project.html", context)


def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'users/student_register.html', {'form': form, 'title': 'reqister here'})


@login_required
def student_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.student)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('student_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentProfileUpdateForm(instance=request.user.student)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)