import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from .models import Job
# Create your views here.


def home(request):
    jobs = Job.objects.all()

    job_data = {}

    for j in jobs:
        lower_bound = j.salary * 0.9
        upper_bound = j.salary * 1.1
        posted = (datetime.datetime.today().date() - j.date_posted).days

        job_data[j.id] = {
            'job': j,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'posted': posted
        }

    return render(request, 'app/hr_dashboard.html', {'job_data':job_data, 'total_jobs': Job.objects.all().count()})


class NewJob(View):

    def get(self, request):
        return render(request, 'app/new_job.html')

    def post(self, request):
        job_title = request.POST.get('jobTitle')
        department = request.POST.get('department')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        introduction = request.POST.get('introduction')
        description = request.POST.get('description')
        responsibilities = request.POST.get('responsibilities')
        qualifications = request.POST.get('qualifications')

        print('job_title:', job_title)
        print('dept:', department)
        print('salary:', salary)
        print('location:', location)
        print('intro:', introduction)
        print('desc:', description)
        print('responsibilities:', responsibilities)
        print('qualifications:', qualifications)

        if job_title:
            if department:
                if salary != '' and int(salary) > 0:
                    if location:
                        if introduction:
                            if description:
                                if responsibilities:
                                    if qualifications:
                                        # Add job to db (CREATE Operation)

                                        new_job = Job.objects.create(job_title=job_title, department=department,
                                                                     salary=salary, location=location,
                                                                     introduction=introduction,
                                                                     brief_posting_description=description,
                                                                     responsibilities=responsibilities,
                                                                     qualifications=qualifications)
                                        new_job.save()
                                        messages.success(request, 'New Job added successfully')
                                        return redirect('home')
                                    else:
                                        messages.warning(request, 'Enter qualifications')
                                else:
                                    messages.warning(request, 'Enter responsibilities')

                            else:
                                messages.warning(request, 'Enter description')
                        else:
                            messages.warning(request, 'Enter an introduction')
                    else:
                        messages.warning(request, 'Enter a valid location')
                else:
                    messages.warning(request, 'Enter a valid salary')
            else:
                messages.warning(request, 'Please add a department')
        else:
            messages.warning(request, 'Please add a job title')

        return render(request, 'app/new_job.html')
