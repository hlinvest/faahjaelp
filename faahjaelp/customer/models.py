from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
   
class Comment(models.Model):
    fromCustomer=models.ForeignKey('Customer')
    toCustomer=models.ForeignKey('Customer', related_name='comment_to_customer')
    comment=models.TextField()
    time=models.DateTimeField()
    class meta:
        ordering=['toCustomer']
        


class Customer(User):                                                      # i weas try to make a customer table before without dependent to User table
    slug=models.SlugField(unique=True)
    description=models.TextField(null=True)
    phone=models.IntegerField(null=True)
    id_verified=models.NullBooleanField()
    picture=models.ImageField(upload_to='media/customer', null=True)
    isWorker=models.BooleanField()
    genre=models.ManyToManyField('job.JobGenre', through='WorkerGenre',null=True )
    

    
    def save(self,*args,**kwargs):                                         #override save method, 
        self.slug=slugify(self.username)                                   #method slugify() Converts to lowercase, removes non-word characters (alphanumerics and underscores) and converts spaces to hyphens. Also strips leading and trailing whitespace.
        super(Customer,self).save(*args, **kwargs)                         #edit username can cause broken links, 
    
    def __unicode__(self):
        return self.username
    

        
    
class WorkerGenre(models.Model):
    worker=models.ForeignKey(Customer)
    genre=models.ForeignKey('job.JobGenre')    
