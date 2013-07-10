# -*- coding: utf-8 -*-                                   
#line above help to show utf8 coding letters,  couldn't understand Non-ASCII character
from django.http import HttpResponseRedirect, HttpResponse
from customer import models
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from customer.forms import RegiForm, LoginForm, ChangeProfile,Picture
from django.contrib.auth import authenticate,login,logout
from customer.models import Customer, WorkerGenre
from job.models import JobGenre, Job
from django.contrib.auth.decorators import login_required


def register(request):
    if request.user.is_authenticated():       # is a section tool
        return HttpResponseRedirect('/profile/')      
    if request.method=='POST': 
        form=RegiForm(request.POST )
        if form.is_valid():
            customer=models.Customer(username=form.cleaned_data['username'], email=form.cleaned_data['email'], description=form.cleaned_data['description'],
                                      phone=form.cleaned_data['phone'], isWorker=form.cleaned_data['isWorker'])
            customer.set_password( form.cleaned_data['password'])
            customer.save()
            if form.cleaned_data['isWorker']:                      # check checkbox value
                    for g in request.POST.getlist('keyword'):
                        genre=JobGenre.objects.get(pk=g)
                        gen=WorkerGenre(worker=customer,genre=genre)
                        gen.save()
            loginForm=LoginForm()           
            return render_to_response('login.html',{'form':loginForm,'text':'færdig med at registere, du kan nu logge in'},context_instance=RequestContext(request))
        else:
            return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    else:
        form=RegiForm() # a blank form
        return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    
def userLogin(request, jobid=None):                                              # don't call it login()
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method=='POST':
        form=LoginForm(request.POST )
        if form.is_valid():   
            username= form.cleaned_data['username']
            password=form.cleaned_data['password' ]
            loginCustomer=authenticate(username=username,password=password)
            if loginCustomer is not None:
                login(request,loginCustomer) 
                if  jobid is not None:
                    return HttpResponseRedirect('/jobvalg/%s/' %jobid)
                else:
                    return HttpResponseRedirect('/profile/')
            else:
                return render_to_response('login.html', {'form':form,'text':'Burgernavn og password passer ikke'},context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form':form},context_instance=RequestContext(request))
    else:
        form=LoginForm()
        return render_to_response('login.html',{'form':form}, context_instance=RequestContext(request))
    
def userLogout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def profile(request):
    customer=Customer.objects.get(id=request.user.id)              # session involved
    print 'the user has id '+ str(request.user.id)
    job=Job.objects.filter(creator=customer)                   # filter return a list, get() return an object
            
    return render_to_response('profile.html',{'customer':customer, 'job':job}, context_instance=RequestContext(request))

@login_required
def edit(request, slug):
    customer=Customer.objects.get(slug=slug)
    if request.user.id != customer.id:
        html="<html><body>du har ikke den id.</body></html>"
        return HttpResponse(html)
    else:
        customer=Customer.objects.get(slug=slug)
        existed_email=customer.email
        keyword=WorkerGenre.objects.filter(worker=customer.id)
        keyword_list=[]
        for k in keyword:
            keyword_list.append(k.genre) 
      
        if request.method=='POST':
            form=ChangeProfile(request.POST,request.FILES,initial={'first_name':customer.first_name, 'last_name':customer.last_name,
                                    'email':customer.email,'description':customer.description,'picture':customer.picture,
                                    'phone':customer.phone,'isWorker':customer.isWorker,'keyword':keyword_list}, existed_email=existed_email,)
            if form.is_valid():
                if customer.isWorker:
                    if form.cleaned_data['isWorker']:
                        print " her is yes yes"
                        editCustomer(customer, form)
                        keyword.delete()
                        for k in request.POST.getlist('keyword'):
                            jg=JobGenre.objects.get(pk=k)
                            wg=WorkerGenre(worker=customer,genre=jg)
                            wg.save()
                        
                    else:
                        print " her is yes no"
                        editCustomer(customer, form)  
                        keyword.delete()    
                        id=str(customer.id)
                        print " here is the customer id"+id

                else:
                    print " her is no yes"
                    if form.cleaned_data['isWorker']:
                        editCustomer(customer, form)
                        for k in request.POST.getlist('keyword'):
                            jg=JobGenre.objects.get(pk=k)
                            wg=WorkerGenre(worker=customer,genre=jg)
                            wg.save()         
                    else:
                        print " her is no no"
                        editCustomer(customer, form)
                return render_to_response('edit.html',{'customer':customer, 'form':form,'text':'dit profil er blevet ændret'}, context_instance=RequestContext(request))            
            else:     
                return render_to_response('edit.html',{'customer':customer, 'form':form}, context_instance=RequestContext(request))             
        else: 
            form=ChangeProfile(initial={'first_name':customer.first_name, 'last_name':customer.last_name,
                                    'email':customer.email,'description':customer.description,'picture':customer.picture,
                                    'phone':customer.phone,'isWorker':customer.isWorker,'keyword':keyword_list}, existed_email=existed_email)          
            return render_to_response('edit.html',{'customer':customer, 'form':form}, context_instance=RequestContext(request))
    
def editCustomer(customer,form):  
    customer.first_name=form.cleaned_data['first_name']
    customer.last_name=form.cleaned_data['last_name']
    customer.email=form.cleaned_data['email'] 
    customer.description=form.cleaned_data['description']
    customer.picture=form.cleaned_data['picture']
    customer.phone=form.cleaned_data['phone']
    customer.isWorker=form.cleaned_data['isWorker']
    customer.set_password(form.cleaned_data['password'])
    customer.picture=form.cleaned_data['picture']
    customer.save() 
    
@login_required    
def edit_pic(request,slug):
    customer=Customer.objects.get(slug=slug)
    if request.user.id != customer.id:
        html="<html><body>du har ikke den id.</body></html>"
        return HttpResponse(html)
    else:
        if request.method=='POST':
            form=Picture(request.POST,request.FILES)
            if form.is_valid():
                if 'change' in request.POST:
                    print " we are in change picture now"
                    customer.picture=form.cleaned_data['picture']
                    print str(form.cleaned_data['picture'])
                    customer.save()
                    return render_to_response('editpic.html', {'form':form,'customer':customer,'text':'dit profil billede er ændret'}, context_instance=RequestContext(request))
                    
                elif 'delete' in request.POST:
                    print " we are in delete pciture now"
                    customer.picture.delete()
                    return render_to_response('editpic.html', {'form':form,'customer':customer, 'text':'dit profil billede er slettet'}, context_instance=RequestContext(request))
            else:
                return render_to_response('editpic.html', {'form':form,'customer':customer}, context_instance=RequestContext(request))
        else:
            form=Picture() 
            return render_to_response('editpic.html', {'form':form,'customer':customer}, context_instance=RequestContext(request))
        
def worker(request, worker_type=None):
    if worker_type is None:
        worker=Customer.objects.filter(isWorker=True)
    else:
        gen=JobGenre.objects.get(genre=worker_type)
        worker=Customer.objects.filter(genre=gen) 
    return render_to_response("arbejder.html",{'worker':worker},context_instance=RequestContext(request))

def specificUser(request, slug):
    worker=Customer.objects.get(slug=slug)
    return render_to_response('person.html',{'worker':worker},context_instance=RequestContext(request))
    
def help(request):
    return render_to_response('hjælp.html',context_instance=RequestContext(request) )
    
    

