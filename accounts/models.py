from datetime import date, datetime
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from .helpers import *
from project import settings


datetime.now().date()


class Batch(models.Model):

    batch = models.CharField(max_length=20)

    @staticmethod
    def get_all_years():
        return Batch.objects.all()

    def __str__(self):
        return self.batch


class DepartmentName(models.Model):
    department = models.CharField(max_length=20)

    @staticmethod
    def get_all_departments():
        return DepartmentName.objects.all()

    def __str__(self):
        return self.department


class Division(models.Model):
    div = models.CharField(max_length=2)

    @staticmethod
    def get_all_divisions():
        return Division.objects.all()

    def __str__(self):
        return self.div


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_guide = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_industry_mentor = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_project_creator = models.BooleanField(default=False)


class Team(models.Model):
    team = models.CharField(max_length=20, default=' ')
    members = models.ManyToManyField(User)

    @staticmethod
    def get_all_teams():
        return Team.objects.all()

    def __str__(self):
        return self.team


class Project(models.Model):
    project_name = models.CharField(max_length=80, default=' ')
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    project_description = models.TextField(blank=True)
    department = models.ForeignKey(DepartmentName, on_delete=models.SET_NULL, null=True, blank=True)
    teams = models.ManyToManyField(Team, blank=True, through='Enroll')

    class Meta:
        ordering = ['project_name']

    def __str__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.project_name)
        super(Project, self).save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, default=' ')
    phone_number = models.CharField(max_length=20, default=' ')
    image = models.ImageField(default='user.png', upload_to='profile_pics/')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(DepartmentName, on_delete=models.SET_NULL, null=True)
    div = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    project = models.ManyToManyField(Project, blank=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user)


class Enroll(models.Model):
    enroll = models.CharField(max_length=20, default=' ')
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    guide_or_industry_mentor = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    date_enrolled = models.DateField()

    class Meta:
        ordering = ['enroll']
        unique_together = [['project', 'team']]

    @staticmethod
    def get_all_enrolls():
        return Enroll.objects.all()

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.team)
        super(Enroll, self).save(*args, **kwargs)

    def __str__(self):
        return self.enroll


class RequestedProject(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    requested_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.requested_project)


class Guide(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    faculty_id = models.CharField(max_length=20, default=' ')
    phone_number = models.CharField(max_length=20,default=' ')
    image = models.ImageField(default='user.png', upload_to='profile_pics/')
    department = models.ForeignKey(DepartmentName, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=20, default=' ')
    worked_experience = models.TextField(blank=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user)


class Hod(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    faculty_id = models.CharField(max_length=20, default=' ')
    department = models.ForeignKey(DepartmentName, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, default=' ')
    image = models.ImageField(default='user.png', upload_to='profile_pics/')

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user)


class IndustryMentor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length=20, default=' ')
    image = models.ImageField(default='user.png', upload_to='profile_pics/')
    designation = models.CharField(max_length=20, default=' ')
    worked_experience = models.TextField(blank=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user)


class Coordinator(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    faculty_id = models.CharField(max_length=20, default=' ')
    phone_number = models.CharField(max_length=20, default=' ')
    department = models.ForeignKey(DepartmentName, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=20, default=' ')
    image = models.ImageField(default='user.png', upload_to='profile_pics/')

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user)


class ProjectCreator(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length=20, default=' ')
    image = models.ImageField(default='user.png', upload_to='profile_pics/')

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user)


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message from " + self.name + ' - ' + self.email


STATUS = (
    ('Yet to start', 'Yet to start'),
    ('Working', 'Working'),
    ('Done', 'Done'),

)


submission = (
    ('Not Submitted', 'Not Submitted'),
    ('In Review', 'In Review'),
    ('Rejected', 'Rejected'),
    ('Approved', 'Approved'),

)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    task_name = models.CharField(max_length=80, default=' ')
    task_description = models.TextField(blank=True)
    description = RichTextField()
    reference_file = models.FileField(upload_to='documents/', blank=True)
    reference_link = models.CharField(max_length=80, default=' ', blank=True)
    Duration = models.DurationField()
    task_percentage = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['project', 'task_name']

    def __str__(self):
        return self.task_name

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.task_name)
        super(Task, self).save(*args, **kwargs)


class Status(models.Model):
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    # enrollment = models.CharField(max_length=80, default=' ')
    enrolled_to = models.ForeignKey(Enroll, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    task_start_date = models.DateTimeField(blank=True, null=True)
    today = models.DateTimeField(default=datetime.now, blank=True)
    task_end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Yet to start')
    submission_file = models.FileField(upload_to='documents/', blank=True)
    submission = models.CharField(max_length=20, choices=submission, default='Not Submitted')

    class Meta:
        ordering = ['slug', 'status']
        unique_together = [['enrolled_to', 'task']]

    @staticmethod
    def get_all_statuses():
        return Status.objects.all()

    def __str__(self):
        return f"{self.get_status_display()}"

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.status)
        super(Status, self).save(*args, **kwargs)


class TaskComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True )
    timestamp = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username


