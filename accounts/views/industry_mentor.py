from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from ..forms import *
from verify_email.email_handler import send_verification_email


def industry_mentor_login(request):
    projects = Project.objects.all()
    enrolls = Enroll.objects.all()
    teams = Team.objects.all()

    context = {
        'projects': projects,
        'enrolls': enrolls,
        'teams': teams,
    }

    return render(request, 'users/industry_mentor/home.html', context)


def task_comment_mentor(request):
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

    return redirect(f"/industry_mentor_task_evaluate/598499865149896141{task.id}4562984656519847")


def industry_mentor_evaluate(request, id):
    task = Task.objects.get(id=id)
    enroll = Enroll.objects.all()
    comments = TaskComment.objects.filter(task=task, parent=None)
    replies = TaskComment.objects.filter(task=task).exclude(parent=None)
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
    status_id = Status.objects.get(task_id=task.id)
    obj = get_object_or_404(Status, id=status_id.id)
    form = StatusForm(request.POST or None, instance=obj)
    u_form = StatusUpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        fm = form.save()
        fm.today = datetime.now()
        fm.save()
        um = u_form.save
        um.today = datetime.now()
        um.save()
        return redirect(f"/industry_mentor_task_evaluate/598499865149896141{task.id}4562984656519847")
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
        'form': form,
        'u_form':u_form,

    }
    return render(request, "users/industry_mentor/evaluate_task.html", context)


def industry_mentor_project_view(request, id):
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
    return render(request, "users/industry_mentor/project_view.html", context)


def industry_mentor_register(request):
    if request.method == 'POST':
        form = IndustryMentorRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect('login')
    else:
        form = IndustryMentorRegisterForm()
    return render(request, 'users/industry_mentor_register.html', {'form': form, 'title': 'reqister here'})


@login_required
def industry_mentor_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = IndustryMentorProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.industrymentor)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('industry_mentor_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = IndustryMentorProfileUpdateForm(instance=request.user.industrymentor)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)