from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from ..models import Contact, User


def home(request):
    return render(request, 'users/home.html', {'title': 'index'})


def main(request):
    return render(request, 'users/main.html', {'title': 'index'})


def main2(request):
    return render(request, 'users/main2.html', {'title': 'index'})


def register(request):
    return render(request, 'users/register.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
    return render(request, "users/contact.html")


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            if user.is_student:
                messages.success(request, f' welcome {username} !!')
                return redirect('student')
            if user.is_guide:
                messages.success(request, f' welcome {username} !!')
                return redirect('guide')
            if user.is_hod:
                messages.success(request, f' welcome {username} !!')
                return redirect('hod')
            if user.is_industry_mentor:
                messages.success(request, f' welcome {username} !!')
                return redirect('industry_mentor')
            if user.is_coordinator:
                messages.success(request, f' welcome {username} !!')
                return redirect('coordinator')
            if user.is_project_creator:
                messages.success(request, f' welcome {username} !!')
                return redirect('project_creator')

            messages.success(request, f' welcome {username} !!')
            return redirect('home')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'log in'})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'Stack Library', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ('password_reset_done')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset.html", context={"password_reset_form":password_reset_form})