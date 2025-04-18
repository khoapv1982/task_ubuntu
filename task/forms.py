from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList  
from .models import task_model

class taskForm(forms.ModelForm):
    class Meta:
        model = task_model
        fields = ['name','date_start','date_plan','date_finish','evidence','report','urgent','update_progress']
        #fields = ['date_finish','evidence','report']
        widgets = { 'name': forms.TextInput(attrs={'style': 'width: 700px;', 'placeholder': 'in put task information'}), 
                   'date_start' : forms.DateInput(attrs={'type' : 'date'}),'date_plan' : forms.DateInput(attrs={'type' : 'date'}),           
                   'evidence': forms.FileInput(attrs={'style': 'width: 200px; margin-left: 10px'}),
                   'report': forms.FileInput(attrs={'style': 'width: 200px; margin-left: 25px'}),  
                   'urgent': forms.CheckboxInput(attrs={'style': 'transform: scale(2);margin-left: 20px'}),
                   'update_progress': forms.TextInput(attrs={'style': 'width: 700px;'}),                 
                   'date_finish' : forms.DateInput(attrs={'type' : 'date'} ),
                   }
           
class taskFormApprove(forms.ModelForm):
    class Meta:
        model = task_model
        fields = ['approvebyleader','rejectbyleader','commentbyleader']
        #fields = ['date_finish','evidence','report']
        widgets = { 'name': forms.TextInput(attrs={'style': 'width: 700px;', 'placeholder': 'in put task information'}), 
                   'date_start' : forms.DateInput(attrs={'type' : 'date'}),'date_plan' : forms.DateInput(attrs={'type' : 'date'}),           
                   'evidence': forms.FileInput(attrs={'style': 'width: 200px; margin-left: 10px'}),
                   'report': forms.FileInput(attrs={'style': 'width: 200px; margin-left: 25px'}),  
                   'urgent': forms.CheckboxInput(attrs={'style': 'transform: scale(2);margin-left: 20px'}),
                   'update_progress': forms.TextInput(attrs={'style': 'width: 700px;'}),                 
                   'date_finish' : forms.DateInput(attrs={'type' : 'date'} ),
                   'approvebyleader': forms.CheckboxInput(attrs={'ID': 'approvebyleader','style': 'transform: scale(2);margin-left: 20px'}),
                   'rejectbyleader': forms.CheckboxInput(attrs={':ID': 'rejectbyleader','style': 'transform: scale(2);margin-left: 33px'}),
                   'commentbyleader': forms.TextInput(attrs={'style': 'width: 700px;margin-left: 3px'}),
                   }
class taskFormadd(forms.ModelForm):
    checkbox_1 = forms.BooleanField(
    required=False, 
    label="Weekly task",
    widget=forms.CheckboxInput(attrs={':ID': 'checkbox_1','style': 'margin-left: 40px'})
    )

    checkbox_2 = forms.BooleanField(
    required=False, 
    label="Monthly task",
    widget=forms.CheckboxInput(attrs={':ID': 'checkbox_2','style': 'margin-left: 37px'})
    )
    
    checkbox_3 = forms.BooleanField(
    required=False, 
    label="Quarterly task",
    widget=forms.CheckboxInput(attrs={':ID': 'checkbox_3','style': 'margin-left: 28px'})
    )

    checkbox_4 = forms.BooleanField(
    required=False, 
    label="Yearly task",
    widget=forms.CheckboxInput(attrs={':ID': 'checkbox_4','style': 'margin-left: 46px'})
    )
    
    class Meta:
        model = task_model       
        fields = ['name','urgent', 'date_start', 'date_plan','date_alarm', 'evidence','report']
        labels = { 'name': 'Task name', 'urgent' : 'Urgent' }
        widgets = {'date_start': forms.DateInput(attrs={'type': 'date', 'style': 'margin-left: 8px'}),
            'date_plan': forms.DateInput(attrs={'type': 'date', 'style': 'margin-left: 8px', 'id': 'date_plan', 'onchange': 'updateDateAlarm()'}),
            'date_alarm': forms.DateInput(attrs={'type': 'date', 'id': 'date_alarm'}),
                   'name': forms.TextInput(attrs={'style': 'width: 700px;', 'placeholder': 'in put task information'}), 
                   'urgent': forms.CheckboxInput(attrs={'style' : 'margin-left: 40px;', 'style': 'width: 70px;'}),    
                    'evidence': forms.FileInput(attrs={'style': 'width: 700px; margin-left: 10px'}),              
                    'report': forms.FileInput(attrs={'style': 'width: 700px; margin-left: 25px'}), 
                  }
        
    
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class taskFormassign(forms.ModelForm):
    class Meta:
        model = task_model
        fields = ['name', 'urgent', 'date_start', 'date_plan', 'date_alarm', 'evidence', 'report', 'employee_id']
        labels = {
            'name': 'Task name',
            'urgent': 'Urgent'
        }
        
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date', 'style': 'margin-left: 8px'}),
            'date_plan': forms.DateInput(attrs={'type': 'date', 'style': 'margin-left: 8px', 'id': 'date_plan', 'onchange': 'updateDateAlarm()'}),
            'date_alarm': forms.DateInput(attrs={'type': 'date', 'id': 'date_alarm'}),
            'name': forms.TextInput(attrs={'style': 'width: 700px;', 'placeholder': 'Nhập thông tin nhiệm vụ'}),
            'urgent': forms.CheckboxInput(attrs={'style': 'margin-left: 40px; width: 70px;'}),
            'evidence': forms.FileInput(attrs={'style': 'width: 700px; margin-left: 10px'}),
            'report': forms.FileInput(attrs={'style': 'width: 700px; margin-left: 25px'}),
            'employee_id': forms.TextInput(attrs={'id': 'Ma_NV', 'style': 'width: 200px;', 'placeholder': 'Mã nhân viên được giao'}),
        }
class DateFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date',"id": "start_date"})
    )
    end_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date',"id": "end_date"})
    )

