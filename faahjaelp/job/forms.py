# -*- coding: utf-8 -*-   
from django.forms.models import ModelForm
from job.models import Job
from django import forms
from faahjaelp import settings
import imghdr
class CreateJob(ModelForm):    
    start_time=forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    end_time=forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    picture=forms.FileField(required=False)
    
    def clean_picture(self):
        picture=self.cleaned_data['picture']
        if picture is not None:
            print picture
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
        model=Job
        exclude=('creator','questions')