from dataclasses import field
from tkinter.ttk import Widget
from django.forms import ModelForm
from django import forms
from .models import Project , Review

class ProjectForm(ModelForm):
    class Meta :
        model = Project
        fields = ['title', 'featured_image','description','demo_link','source_link']

        widgets ={
            'tags' : forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        for key,value in self.fields.items() :
            value.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']

        labels = {
            'value':'Place your vote',
            'body':'Add comment with your vote'
        }
    def __init__(self, *args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        for key,value in self.fields.items() :
            value.widget.attrs.update({'class':'input'})
    