from django.db import models
from customer.models import Customer

class JobGenre(models.Model):
    genre=models.CharField(max_length=40) # max_length is the required argument
    def __unicode__(self):
        return self.genre
    
class Image(models.Model):
    toJob=models.ForeignKey('Job', verbose_name=' images to the job with id') # foreign key, represent many to one relationship,  use a class that havn't been defined
    image=models.ImageField(upload_to='media/job')
    
class Question(models.Model):
    toJob=models.ForeignKey('Job', verbose_name='questions to the job with id')
    question=models.TextField()
    answer=models.TextField()
    
    class Meta:
        ordering=["toJob"]
        
    

class Job(models.Model):
    title=models.CharField(max_length=40)
    genre=models.ManyToManyField(JobGenre, through='GenreToJob')   # many to many relation, a job can have many genre and a genre can give to many jobs
    creator=models.ForeignKey(Customer)
    location=models.TextField()
    start_time=models.DateTimeField()             
    end_time=models.DateTimeField()
    description=models.TextField()
    reward=models.CharField(max_length=100, null=True)
    isActive=models.BooleanField(default=True)
    picture=models.ImageField(upload_to='media/job', null=True)     
    questions=models.ForeignKey(Question,null=True )
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering=['-end_time','creator']
        
class GenreToJob(models.Model):
    job=models.ForeignKey(Job)
    genre=models.ForeignKey(JobGenre)
        
#class PassJob(models.Model):                                       # cannot overwrite a field in Django, 
#    id_for_job= models.IntegerField(primary_key=True)
#    title=models.CharField(max_length=40)
#    genre=models.ManyToManyField(JobGenre)   
#    creator=models.ForeignKey(Customer)
#    location=models.TextField()
#    start_time=models.DateTimeField()             
#    end_time=models.DateTimeField()
#    description=models.TextField()
#    reward=models.TextField(null=True)
#    
#    class meta:
#        ordering=['end_time']
#        
#    def __unicode__(self):
#        return self.title
#    
    

    
    
    
    
