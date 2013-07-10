# -*- coding: utf-8 -*-  
from django.conf.urls import patterns, include, url
from django.contrib import admin
from faahjaelp import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
admin.autodiscover()                                    #used admin.autodiscover() to automatically load the INSTALLED_APPS admin.py modules

urlpatterns = patterns('customer.views',    #avoid redundancy                     
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^logout/$', 'userLogout'),
    (r'^admin/', include(admin.site.urls)),    
    (r'^register/$','register'),                          # can also import the view module and add the method here instead of a string
     (r'^login/$','userLogin'),
    (r'^login/(?P<jobid>.*)/$','userLogin'),
    (r'^profile/$','profile'),
    (r'^hjaelp/$','help'),
    (r'edit/(?P<slug>.*)/$', 'edit'),
    (r'edit_pic/(?P<slug>.*)/$', 'edit_pic'),
    (r'^arbejder/(?P<worker_type>[\w|\W]+)/$', 'worker'),
    (r'^arbejder/$', 'worker'),
    (r'^arbejder/bruger/(?P<slug>.*)/$', 'specificUser'),
    
    

)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+= patterns('job.views', 
     url(r'^$', 'index'), 
     (r'^profile/addJob/$', 'addJob'),
     (r'editjob/(?P<jobid>.*)/$', 'editJob'),
     (r'^jobvalg/(?P<jobid>.*)/$','jobValg'),
    (r'^job/(?P<jobtype>[\w|\W]+)/$', 'index'),        # allow space in url, ^(?P<jobtype>\w+)/ wont take space
                       )

urlpatterns+=staticfiles_urlpatterns() 
