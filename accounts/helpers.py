from django.utils.text import slugify 

import string
import random


def generate_random_string(N): 
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    return res
  

def generate_slug(text):
    new_slug = slugify(text)
    from .models import Project, Task, Enroll, Status
    
    if Project.objects.filter(slug = new_slug).first():
        return generate_slug(text + generate_random_string(5))
    elif Task.objects.filter(slug = new_slug).first():
        return generate_slug(text + generate_random_string(5))
    elif Enroll.objects.filter(slug = new_slug).first():
        return generate_slug(str(text) + generate_random_string(7))
    elif Status.objects.filter(slug = new_slug).first():
        return generate_slug(str(text) + generate_random_string(5))
    return new_slug
