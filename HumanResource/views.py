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


class EditJob(View):
    def get(self, request, job_id):
        job = Job.objects.filter(id=job_id)[0] # [0] to show the data -in the fields-
        return render(request, 'app/edit_job.html', locals())
    
    def post(self, request, job_id):
        job = Job.objects.filter(id=job_id)[0]

        job_title = request.POST.get('jobTitle')
        department = request.POST.get('department')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        introduction = request.POST.get('introduction')
        description = request.POST.get('description')
        responsibilities = request.POST.get('responsibilities')
        qualifications = request.POST.get('qualifications')
        is_active = request.POST.get('recruiting')

        if job_title:
            if department:
                if salary != '' and int(salary) > 0:
                    if location:
                        if introduction:
                            if description:
                                if responsibilities:
                                    if qualifications:
                                        # Update job to db

                                        try:
                                            job.job_title = job_title
                                            job.department = department
                                            job.salary = salary
                                            job.location = location
                                            job.introduction = introduction
                                            job.brief_posting_description = description
                                            job.responsibilities = responsibilities
                                            job.qualifications = qualifications
                                            job.is_active = is_active
                                            job.save()
                                            messages.success(request, 'Job Updated Successfully')
                                            return redirect('home')

                                        except Exception as e:
                                            print(e)
                                            messages.warning(request, 'Job Update not successful')

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

        return render(request, 'app/edit_job.html')


def careers(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'app/careers.html', locals())

def job_detail_page(request, job_id):
    try:
        job = Job.objects.filter(id=job_id)[0]
        return render(request, 'app/job_detail.html', locals())

    except Exception as e:
        print(e)
        return HttpResponse('Job Not found')