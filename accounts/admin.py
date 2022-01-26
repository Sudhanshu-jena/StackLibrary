from django.contrib import admin
from .models import User, TaskComment, Student, Status, Guide, Hod, \
    IndustryMentor, Coordinator, ProjectCreator, Contact, Batch, DepartmentName, \
    Division, Team, Project, Task, Enroll, RequestedProject


class AdminStudent(admin.ModelAdmin):
    list_display = ['user', 'batch']


class AdminGuide(admin.ModelAdmin):
    list_display = ['user']


class AdminIndustryMentor(admin.ModelAdmin):
    list_display = ['user']


class AdminHod(admin.ModelAdmin):
    list_display = ['user']


class AdminProjectCreator(admin.ModelAdmin):
    list_display = ['user']


class AdminCoordinator(admin.ModelAdmin):
    list_display = ['user']


class AdminYear(admin.ModelAdmin):
    list_display = ['batch']


class AdminDivision(admin.ModelAdmin):
    list_display = ['div']


class AdminDepartmentName(admin.ModelAdmin):
    list_display = ['department']


class AdminEnrollName(admin.ModelAdmin):
    list_display = ['enroll', 'project', 'team']


class AdminEnrollmentName(admin.ModelAdmin):
    list_display = ['task', 'status', 'enrolled_to']


class AdminTaskName(admin.ModelAdmin):
    list_display = ['task_name', 'project']


admin.site.register(User)
admin.site.register(TaskComment)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(RequestedProject)
admin.site.register(Status, AdminEnrollmentName)
# admin.site.register(Reply)
admin.site.register(Enroll, AdminEnrollName)
admin.site.register(Task, AdminTaskName)
admin.site.register(Student, AdminStudent)
admin.site.register(Guide, AdminGuide)
admin.site.register(Hod, AdminHod)
admin.site.register(IndustryMentor, AdminIndustryMentor)
admin.site.register(ProjectCreator, AdminProjectCreator)
admin.site.register(Coordinator, AdminCoordinator)
admin.site.register(Contact)
admin.site.register(Batch, AdminYear)
admin.site.register(DepartmentName, AdminDepartmentName)
admin.site.register(Division, AdminDivision)