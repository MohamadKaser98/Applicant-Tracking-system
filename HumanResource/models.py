from django.db import models

# Create your models here.

departments = (('HR', 'Human Resource'), ('IT', 'Information Technology'), ('Marketing', 'Marketing'),
               ('Finance', 'Finance'), ('R&D', 'Research and Development'))

locations = (('Nairobi, Kenya', 'Nairobi, Kenya'), ('California, US', 'California, US'),
             ('London, UK', 'London, UK'), ('San fransisco, US', 'San fransisco, US'),
             ('Cape Town, SA', 'Cape Town, SA'))

genders = (('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say'))

class Job(models.Model):
    job_title = models.CharField(max_length=100, null=False)
    department = models.CharField(max_length=50, choices=departments)
    salary = models.IntegerField()
    location = models.CharField(max_length=100, choices=locations)
    introduction = models.CharField(max_length=220)
    brief_posting_description = models.CharField(max_length=400)
    responsibilities = models.CharField(max_length=3000)
    qualifications = models.CharField(max_length=1500)

    is_active = models.BooleanField(default=True)
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.job_title