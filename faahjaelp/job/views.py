# -*- coding: utf-8 -*-      
from job.models import Job, GenreToJob, JobGenre
from datetime import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from job.forms import CreateJob
from job import models
from django.http import HttpResponseRedirect, HttpResponse
from customer.models import Customer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request, jobtype=None):
    #jobs=Job.objects.exclude(end_time__lte =datetime.now(), isActive=True) # gte greater, lte less
    if jobtype is None:
        jobs=Job.objects.filter( end_time__gte =datetime.now(), isActive=True).order_by('start_time')
    else:
        gen=JobGenre.objects.get(genre=jobtype)
        jobs=Job.objects.filter( end_time__gte =datetime.now(),genre=gen, isActive=True).order_by('start_time')      # cannot directly use jobtype because genre is an integer here.
#    paginator=Paginator(jobs, 2)
#    page=request.GET.get('page')
#    try:
        
    return render_to_response('index.html', {'jobs':jobs, 'jobtype':jobtype}, context_instance=RequestContext(request))

@login_required
def addJob(request):
    customer=Customer.objects.get(pk=request.user.id)
    if request.method=='POST':
        form=CreateJob(request.POST,request.FILES)
        print  datetime.now().strftime('%y-%m-%d %H:%M')
        if form.is_valid():
            job=models.Job(title=form.cleaned_data['title'], start_time=form.cleaned_data['start_time'], end_time=form.cleaned_data['end_time'], 
                           reward=form.cleaned_data['reward'], description=form.cleaned_data['description'], isActive=form.cleaned_data['isActive'],
                           location=form.cleaned_data['location'],creator=customer, picture=form.cleaned_data['picture'])   
            job.save()
            for g in request.POST.getlist('genre'):
                genre=JobGenre.objects.get(pk=g)
                gen=GenreToJob(job=job, genre=genre)
                gen.save()
            return render_to_response('addJob.html',{'form':form,'text': 'jobben er tilføjet, tilføj et ny ved rette på informationer','customer':customer  },context_instance=RequestContext(request))
        else:
            return render_to_response('addJob.html',{'form':form, 'text': 'mangler information', 'customer':customer  },context_instance=RequestContext(request))
        
    else:
        form=CreateJob()
        return render_to_response('addJob.html',{'form':form, 'customer':customer },context_instance=RequestContext(request))
    
@login_required
def editJob(request, jobid):
    if request.user.id != Job.objects.get(id=jobid).creator_id:
        html="<html><body>du har ikke et job med det id.</body></html>"
        return HttpResponse(html)
    else:        
        job=Job.objects.get(pk=jobid)
        time_format='%Y-%m-%d %H:%M'
        gens=GenreToJob.objects.filter(job_id=job.id)
        gens_list=[]
        for g in gens:
            gens_list.append(g.genre)
            print g.genre
        if request.method=='POST':
            form=CreateJob(request.POST, request.FILES,initial={'title':job.title,'genre':gens_list,'start_time':job.start_time.strftime(time_format),
                                                 'end_time':job.end_time.strftime(time_format),'reward':job.reward, 'description':job.description, 
                                                 'isActive':job.isActive,'location':job.location,'picture':job.picture})
            if form.is_valid():
                if 'change' in request.POST:
                    job.title=form.cleaned_data['title']
                    job.start_time=form.cleaned_data['start_time']
                    job.end_time=form.cleaned_data['end_time']
                    job.reward=form.cleaned_data['reward']
                    job.description=form.cleaned_data['description']
                    job.isActive=form.cleaned_data['isActive']
                    job.location=form.cleaned_data['location']
                    job.picture=form.cleaned_data['picture']
                    job.save()
                    gens.delete()
                    for g in request.POST.getlist('genre'):
                            genre=JobGenre.objects.get(pk=g)
                            gen=GenreToJob(job=job,genre=genre)
                            gen.save()
                    return render_to_response('editjob.html',{'form':form, 'text':'ændring er registeret'}, context_instance=RequestContext(request))
                elif 'delete' in request.POST:
                    job.delete()
                    return HttpResponseRedirect('/profile/')
            else:
                return render_to_response('editjob.html',{'form':form, 'text':'udføre korrekt information'}, context_instance=RequestContext(request))
        else:
            
            form=CreateJob(initial={'title':job.title,'genre':gens_list,'start_time':job.start_time.strftime(time_format),'end_time':job.end_time.strftime(time_format),
                                                 'reward':job.reward, 'description':job.description, 'isActive':job.isActive,'location':job.location,'picture':job.picture})
            return render_to_response('editjob.html',{'form':form, 'text':'ændrer oplysning til jobbet here'}, context_instance=RequestContext(request))

def jobValg(request, jobid):
    job= Job.objects.get(pk=jobid)
    customer=Customer.objects.get(pk=job.creator_id)
    print"customer is "+ customer.username
    return render_to_response("jobvalg.html", {'job':job,'customer': customer}, context_instance=RequestContext(request))           
    