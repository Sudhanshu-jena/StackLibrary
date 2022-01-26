from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth
from django.conf.urls.static import static
from accounts.views import login as user_view
from accounts.views import student as student_view
from accounts.views import guide as guide_view
from accounts.views import coordinator as coordinator_view
from accounts.views import hod as hod_view
from accounts.views import industry_mentor as industry_mentor_view
from accounts.views import project_creator as project_creator_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('login/', user_view.Login, name='login'),
    path('student/', student_view.student_login, name='student'),
    path('student_pro/', student_view.student_project, name='student_pro'),
    path('guide/', guide_view.guide_login, name='guide'),
    path('coordinator/', coordinator_view.coordinator_login, name='coordinator'),
    path('industry_mentor/', industry_mentor_view.industry_mentor_login, name='industry_mentor'),
    path('project_creator/', project_creator_view.project_creator_login, name='project_creator'),
    path('hod/', hod_view.hod_login, name='hod'),
    path('home/', student_view.student_login, name='home'),
    path('logout/', auth.LogoutView.as_view(template_name='users/main.html'), name='logout'),
    path('guide_profile/', guide_view.guide_profile, name='guide_profile'),
    path('student_profile/', student_view.student_profile, name='student_profile'),
    path('hod_profile/', hod_view.hod_profile, name='hod_profile'),
    path('coordinator_profile/', coordinator_view.coordinator_profile, name='coordinator_profile'),
    path('industry_mentor_profile/', industry_mentor_view.industry_mentor_profile, name='industry_mentor_profile'),
    path('project_creator_profile/', project_creator_view.project_creator_profile, name='project_creator_profile'),
    path('register/', user_view.register, name='register'),
    path('student_register/', student_view.student_register, name='student_register'),
    path('guide_register/', guide_view.guide_register, name='guide_register'),
    path('hod_register/', hod_view.hod_register, name='hod_register'),
    path('industry_mentor_register/', industry_mentor_view.industry_mentor_register, name='industry_mentor_register'),
    path('project_creator_register/', project_creator_view.project_creator_register, name='project_creator_register'),
    path('coordinator_register/', coordinator_view.coordinator_register, name='coordinator_register'),
    path('verification/', include('verify_email.urls')),
    path('accounts/login/', user_view.Login, name='accounts/login/'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('', include('accounts.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)