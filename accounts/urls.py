from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login
from .views.student import student_team_create, student_project, student_team_view, view_team, \
    student_detail_view, request_project, student_enroll_details, task_view, task_comment_student, \
    request_project_confirm
from .views.industry_mentor import industry_mentor_project_view, industry_mentor_evaluate, task_comment_mentor
from .views.guide import guide_project_view, guide_evaluate, task_comment_guide
from .views.coordinator import coordinator_progress_view, coordinator_requested_project, coordinator_edit_project, \
    coordinator_assigned_project, update_enroll_view, coordinator_detail_view, view_enroll_details, \
    coordinator_enroll_project
from .views.hod import hod_detail_view, hod_enroll_details
from .views.project_creator import project_creator_add_task, new_project, detail_view, update_view, \
    update_task_view, delete_task_view, delete_project_view


urlpatterns = [
    path('', login.main, name='main'),
    path('main2/', login.main2, name='main2'),
    path('contact/', login.contact, name='contact'),
    path('student_team_create/', student_team_create, name='student_team_create'),
    path('student_team_view/', student_team_view, name='student_team_view'),
    path('student_project/', student_project, name='student_project'),
    path('request_project_confirm/79888411541545<int:id>78961794517489451', request_project_confirm, name='request_project_confirm'),
    path('request_project/', request_project, name='request_project'),
    path('industry_mentor_project_view/859198485598498498595<int:id>49404151', industry_mentor_project_view, name='industry_mentor_project_view'),
    path('industry_mentor_task_evaluate/598499865149896141<int:id>4562984656519847', industry_mentor_evaluate, name='industry_mentor_task_evaluate'),
    path('guide_project_view/5648749846515619494165<int:id>84984898498451/', guide_project_view, name='guide_project_view'),
    path('guide_task_evaluate/56184984165484984981<int:id>4562984656519847', guide_evaluate, name='guide_task_evaluate'),
    path('coordinator_assigned_project/', coordinator_assigned_project, name='coordinator_assigned_project'),
    path('coordinator_enroll_project/88468465149461<int:id>9849684816641', coordinator_enroll_project, name='coordinator_enroll_project'),
    path('coordinator_edit_project/', coordinator_edit_project, name='coordinator_edit_project'),
    path('coordinator_progress_view/7449498465179<int:id>84985984151941745', coordinator_progress_view, name='coordinator_progress_view'),
    path('task_view/8464648651684118<int:id>4846474141146', task_view, name='task_view'),
    path('task_comment_student', task_comment_student, name="task_comment_student"),
    path('task_comment_guide', task_comment_guide, name="task_comment_guide"),
    path('task_comment_mentor', task_comment_mentor, name="task_comment_mentor"),
    path('coordinator_requested_project/', coordinator_requested_project, name='coordinator_requested_project'),
    path('project_creator_add_task/', project_creator_add_task, name='project_creator_add_task'),
    path('project_creator_create_project/', new_project, name='project_creator_create_project'),
    path('project_creator/<slug:slug>/', detail_view),
    path('coordinator/<slug:slug>/', coordinator_detail_view),
    path('hod_detail_view/view_<slug:slug>_project_details/', hod_detail_view, name='hod_detail_view'),
    path('student_detail_view/786498490567823647467849<int:id>6678933446613/', student_detail_view, name='student_detail_view'),
    path('786498490567823647467849<int:id>/', update_view, name='update_view' ),
    path('6521456588551<int:id>786498490567823647467849/update', update_task_view, name='update_task_view' ),
    path('42153454944<int:id>6498469884194984/full_details', view_enroll_details, name='view_enroll_details' ),
    path('984984849418421534<int:id>749448494/hod_enroll_details', hod_enroll_details, name='hod_enroll_details' ),
    path('34313534351<int:id>786498490567823647467849/student_enroll_details', student_enroll_details, name='student_enroll_details' ),
    path('15333231<int:id>786498490567823647467849/view_team', view_team, name='view_team' ),
    path('534643153<int:id>786498490567823647467849/delete_task', delete_task_view, name='delete_task_view'),
    path('4868643154<int:id>786498490567823647467849/delete_project', delete_project_view, name='delete_project_view'),
    path('348664613147686<int:id>786498490567823647467849/update_enroll_view', update_enroll_view, name='update_enroll_view'),
    path("password_reset", login.password_reset_request, name="password_reset"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)