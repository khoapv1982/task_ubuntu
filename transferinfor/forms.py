from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList  
from .models import transferinfor_model

class transformadd(forms.ModelForm):    
    class Meta:
        model = transferinfor_model       
        fields = ['trans_title','trans_content','trans_images','trans_report','trans_receiver','trans_team_receiver','trans_dept_receiver']
        # labels = { 'name': 'Task name', 'urgent' : 'Urgent' }
        widgets ={ 'trans_title': forms.TextInput(attrs={'style': 'width: 700px; margin-left: 75px',  'placeholder': 'in put trans title'}),
                   'trans_content': forms.TextInput(attrs={'style': 'width: 700px; margin-left: 50px',  'placeholder': 'in put trans information'}),
                   'trans_images': forms.FileInput(attrs={'style': 'width: 700px; margin-left: 50px'}),                                      
                   'trans_report': forms.FileInput(attrs={'style': 'width: 700px; margin-left: 55px'}),                   
                   'trans_receiver': forms.TextInput(attrs={'style': 'width: 700px; margin-left: 45px',  'placeholder': 'in put partner ID to share'}),
                   'trans_team_receiver': forms.TextInput(attrs={'style': 'width: 300px; margin-left: 10px',  'placeholder': 'in put Team ID to share'}),
                   'trans_dept_receiver': forms.TextInput(attrs={'style': 'width: 300px; margin-left: 10px',  'placeholder': 'in put Dept ID to share'}), }           


       
                  
        