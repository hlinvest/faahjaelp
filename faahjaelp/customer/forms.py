# -*- coding: utf-8 -*-   
from django.forms.models import ModelForm
from customer.models import Customer
from django import forms
from job.models import JobGenre
from faahjaelp import settings
import imghdr


class RegiForm(ModelForm):
    password=forms.CharField(label=(u'password'), widget=forms.PasswordInput(render_value=False))
    password2=forms.CharField(label=(u'password2'), widget=forms.PasswordInput(render_value=False))
    keyword=forms.ModelMultipleChoiceField(required=False, queryset=JobGenre.objects.all())
    class Meta:
        model=Customer
        exclude=('picture','last_login', 'id_verified','slug','date_joined','genre')
        
    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            Customer.objects.get(username=username)
        except Customer.DoesNotExist:
                return username      
        raise forms.ValidationError('brugernavn er optaget.')
    
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return email
        raise forms.ValidationError("den email er optaget.")
      
    def clean_password(self):
        password=self.cleaned_data.get('password',None)
        print password
        if len(password)<6:
            raise forms.ValidationError('password skal minimun være 6 tegn')
        return password
        
    def clean(self):
        password=self.cleaned_data.get('password',None)                                                       #instead of use cleaned_data, use get here to avoid exception when nothing is return, none is the default value
        password2=self.cleaned_data.get('password2',None)
        
        if password and password and (password2 == password):
            return self.cleaned_data                                                                             # this method has access too all the fields in the class, so it must return all the fields instead of one.        
        raise forms.ValidationError('to indtastede passsword er ikke ens')

class ChangeProfile(RegiForm):
    picture= forms.FileField(required=False)
    def __init__(self, *args, **kwargs):                                       
        self.existed_email=kwargs.pop('existed_email')                           # too add a extra arguament to the class
        super(ChangeProfile, self).__init__(*args,**kwargs)
    def clean_email(self):
        print 'the existed email is '+ self.existed_email
        email=self.cleaned_data['email']
        if email!=self.existed_email:
            try:
                Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return email
            raise forms.ValidationError("den email er optaget.")
        return email
    
        
    def clean_picture(self):
        picture=self.cleaned_data['picture']
        if picture is not None:
            if imghdr.what(picture):
                if  picture.size> settings.MAX_PIC_SIZE:
                    raise forms.ValidationError('Billedet er for stor, max størrelse på billede er  '+str(settings.MAX_PIC_SIZE)+"bit")
                else:
                    return picture
            else:
                    raise forms.ValidationError(' det er ikke et billede file')
        else:
            return None
            
            
    class Meta:
        model=Customer
        exclude={'username','id_verified','slug','last_login','date_joined'}
        
class Picture(forms.Form):
        picture=forms.FileField(required=False)
        
        def clean_picture(self):
            picture=self.cleaned_data['picture']
            if picture is not None:
                if imghdr.what(picture):
                    if  picture.size> settings.MAX_PIC_SIZE:
                        raise forms.ValidationError('Billedet er for stor, max størrelse på billede er  '+str(settings.MAX_PIC_SIZE)+"bit")
                    else:
                        return picture
                else:
                        raise forms.ValidationError(' det er ikke et billede file')
            else:
                return None
            
    
class LoginForm(forms.Form):                                                                                      # here doesn't need to extend any model
        username=forms.CharField(label=(u'username'))
        password=forms.CharField(label=(u'password'), widget=forms.PasswordInput(render_value=False))
      
        

         
            