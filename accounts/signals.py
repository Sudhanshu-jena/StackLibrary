from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Student, Guide, IndustryMentor, Coordinator, Hod, ProjectCreator


@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_student(sender, instance, **kwargs):
    instance.student.save()


@receiver(post_save, sender=User)
def create_guide(sender, instance, created, **kwargs):
    if created:
        Guide.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_guide(sender, instance, **kwargs):
    instance.guide.save()


@receiver(post_save, sender=User)
def create_hod(sender, instance, created, **kwargs):
    if created:
        Hod.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_hod(sender, instance, **kwargs):
    instance.hod.save()


@receiver(post_save, sender=User)
def create_project_creator(sender, instance, created, **kwargs):
    if created:
        ProjectCreator.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_project_creator(sender, instance, **kwargs):
    instance.project_creator.save()


@receiver(post_save, sender=User)
def create_coordinator(sender, instance, created, **kwargs):
    if created:
        Coordinator.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_coordinator(sender, instance, **kwargs):
    instance.coordinator.save()


@receiver(post_save, sender=User)
def create_industry_mentor(sender, instance, created, **kwargs):
    if created:
        IndustryMentor.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_industry_mentor(sender, instance, **kwargs):
    instance.industry_mentor.save()