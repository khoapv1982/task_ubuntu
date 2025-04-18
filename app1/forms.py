from django import forms
from .models import department as department_model, team as team_model
from employees.models import employee_model
from task.models import task_model

class department_form(forms.ModelForm):
    class Meta:
        model=department_model
        fields=['department_id','name','manager_dep']
        widgets = {'department_id': forms.TextInput(attrs={'style': 'width: 200px; margin-left: 0px'}),
                    'name': forms.TextInput(attrs={'style': 'width: 200px; margin-left: 50px'}), 
                   'manager_dep': forms.TextInput(attrs={'style': 'width: 200px; margin-left: 4px'}),
                  }

class team_form(forms.ModelForm):
    class Meta:
        model=team_model
        fields=['department_id','manager_dep','team_id','name','team_leader']
        widgets = {'department_id': forms.TextInput(attrs={'id': 'Ma_phong','style': 'width: 200px; margin-left: 1px'}),
                   'manager_dep': forms.TextInput(attrs={'id': 'ID_manager_dept','style': 'width: 200px; margin-left: 7px'}),
                    'team_id': forms.TextInput(attrs={'id': 'Ma_team','style': 'width: 200px; margin-left: 42px'}),
                    'name': forms.TextInput(attrs={'style': 'width: 200px; margin-left: 54px'}),                                                             
                    'team_leader': forms.TextInput(attrs={'id': 'Ma_leader','style': 'width: 200px; margin-left: 12px'}),
                   
                  }

class employee_form(forms.ModelForm):
    class Meta:
        model=employee_model
        fields=['employee_id','department_id','name']

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class Task_form(forms.ModelForm):
    class Meta:
        model=task_model
        fields=['task_id','name','date_start','date_plan','date_finish','employee_id','department_id','leader','evidence','report','urgent']
    