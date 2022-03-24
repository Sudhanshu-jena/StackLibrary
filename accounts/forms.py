from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import *

USER_TYPE = [
    ('STUDENT', 'Student'),
    ('GUIDE', 'Guide'),
    ('HOD', 'Hod'),
    ('INDUSTRY MENTOR', 'Industry Mentor'),
    ('PROJECT CREATOR', 'Project Creator'),
    ('COORDINATOR', 'Coordinator'),
]


class StudentTeamForm(forms.ModelForm):
    team = models.CharField(max_length=20, default=' ')

    class Meta:
        model = Team
        fields = '__all__'

    @transaction.atomic
    def save(self, commit=True):
        team = super().save()

        team.save()
        return team


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user


class GuideRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_guide = True
        user.save()
        guide = Guide.objects.create(user=user)
        guide.save()
        return user


class ProjectCreatorRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_project_creator = True
        user.save()
        project_creator = ProjectCreator.objects.create(user=user)
        project_creator.save()
        return user


class HodRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_hod = True
        user.save()
        hod = Hod.objects.create(user=user)
        hod.save()
        return user


class CoordinatorRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_coordinator = True
        user.save()
        coordinator = Coordinator.objects.create(user=user)
        coordinator.save()
        return user


class IndustryMentorRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_industry_mentor = True
        user.save()
        industry_mentor = IndustryMentor.objects.create(user=user)
        industry_mentor.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class StudentProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Student
        fields = ['phone_number', 'image', 'college', 'batch', 'department', 'div']


class GuideProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Guide
        fields = ['faculty_id', 'phone_number', 'image', 'college', 'department', 'designation', 'worked_experience']


class HodProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Hod
        fields = ['faculty_id', 'phone_number', 'image', 'college', 'department']


class ProjectCreatorProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = ProjectCreator
        fields = ['phone_number', 'image']


class CoordinatorProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Coordinator
        fields = ['faculty_id', 'phone_number', 'image', 'college', 'department', 'designation']


class IndustryMentorProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = IndustryMentor
        fields = ['phone_number', 'image', 'designation', 'worked_experience']


class TaskUpdateForm(forms.ModelForm):
    task_name = forms.CharField(max_length=80)

    class Meta:
        model = Task
        fields = '__all__'


class ProjectUpdateForm(forms.ModelForm):
    project_name = forms.CharField(max_length=80)

    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'department', 'college', 'batch']


class TaskRegistrationForm(forms.ModelForm):
    task_name = forms.CharField(max_length=80)

    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'description', 'reference_file', 'Duration', 'task_percentage']

    def save(self, commit=True):
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.task_name = self.cleaned_data['task_name']
        task.save()

        if commit:
            task.save()

        return task

    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['task_name'].widget.attrs['placeholder'] = 'Name'


class ProjectRegistrationForm(forms.ModelForm):
    project_name = forms.CharField(max_length=80)
    project_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'department', 'college', 'batch']

    def save(self, commit=True):
        Project = super(ProjectRegistrationForm, self).save(commit=False)
        Project.project_name = self.cleaned_data['project_name']
        Project.project_description = self.cleaned_data['project_description']
        Project.save()

        if commit:
            Project.save()

        return Project


class DateInput(forms.DateTimeInput):
    input_type = 'date'


class EnrollForm(forms.ModelForm):
    date_enrolled = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = Enroll
        fields = ['enroll', 'team', 'college', 'batch', 'duration', 'guide_or_industry_mentor', 'date_enrolled']


class EnrollForm1(forms.ModelForm):
    date_enrolled = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = Enroll
        fields = '__all__'


class SavedDataForm1(forms.ModelForm):
    date_enrolled = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = Enroll
        fields = '__all__'


class SavedDataForm(forms.ModelForm):
    date_enrolled = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = Enroll
        fields = ['enroll', 'team', 'college', 'batch', 'duration', 'guide_or_industry_mentor', 'date_enrolled']


class EnrollUpdateForm(forms.ModelForm):

    class Meta:
        model = Enroll
        fields = '__all__'


class SavedDataUpdateForm(forms.ModelForm):

    class Meta:
        model = SavedData
        fields = '__all__'


class RequestProjectForm(forms.ModelForm):

    class Meta:
        model = RequestedProject
        fields = ['team', 'batch']


class StatusForm(forms.ModelForm):
    task_start_date = forms.DateTimeField(widget=DateInput)
    task_end_date = forms.DateTimeField(widget=DateInput)

    class Meta:
        model = Status
        fields = ['task', 'task_start_date', 'task_end_date', 'status', 'submission']


class StatusUpdateForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['task', 'status', 'submission']


