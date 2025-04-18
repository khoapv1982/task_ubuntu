from django.db import models
from app1.models import department
from employees.models import employee_model

# Create your models here.
class task_model(models.Model):
    
    task_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500, null=False)
    date_start=models.DateField()
    date_plan=models.DateField()
    date_alarm=models.DateField(null=True,blank=True,default=None)
    date_finish=models.DateField(null=True,blank=True,default=None)
    employee_id=models.CharField()
    department_id=models.IntegerField(null=False,default=None)
    leader=models.CharField(null=False, default=None)
    evidence =models.ImageField(upload_to='images',null=True,blank=True,default=None)
    report=models.FileField(upload_to='files',null=True,blank=True,default=None)
    urgent=models.BooleanField(null=False,default=False)
    team_id=models.CharField(null=False, blank=False, default=None)
    team_leader=models.CharField(null=False, blank=False, default=None)
    manager_dep=models.CharField(null=False, blank=False, default=None)
    date_create=models.DateField(null=True,blank=True,default=None)
    date_edit=models.DateField(null=True,blank=True,default=None)
    ip_client_create=models.CharField(null=True,blank=True,default=None)
    ip_client_edit=models.CharField(null=True,blank=True,default=None)
    note=models.CharField(max_length=500, null=True, blank=True, default=None)
    sent_email=models.CharField(max_length=10, null=True, blank=True, default=None)
    name_old=models.CharField(null=True,blank=True,default=None)
    date_start_old=models.DateField(null=True,blank=True,default=None)
    date_plan_old=models.DateField(null=True,blank=True,default=None)
    date_finish_old=models.DateField(null=True,blank=True,default=None)
    leader_old=models.CharField(null=True,blank=True,default=None)
    evidence_old =models.ImageField(upload_to='images',null=True,blank=True,default=None)
    report_old=models.FileField(upload_to='files',null=True,blank=True,default=None)
    urgent_old=models.BooleanField(null=True,default=False)
    date_edit_old=models.DateField(null=True,blank=True,default=None)
    ip_client_edit_old=models.CharField(null=True,blank=True,default=None)
    email_modify=models.IntegerField(null=True, blank=True, default=None)
    infringe=models.CharField(max_length=10, null=True, blank=True, default=None)
    approvebyleader=models.BooleanField(null=True, blank=True, default=None)
    status=models.IntegerField(null=True, blank=True, default=None)
    update_progress=models.CharField(max_length=2500, null=True, blank=True, default=None)
    progress_old=models.CharField(max_length=2500, null=True, blank=True, default=None)
    rejectbyleader=models.BooleanField(null=True, blank=True, default=None)
    commentbyleader=models.CharField(max_length=1000, null=True, blank=True, default=None)
    email_approve=models.IntegerField(null=True, blank=True, default=None)
    date_approved=models.DateField(null=True,blank=True,default=None)
    date_reject=models.DateField(null=True,blank=True,default=None)
    email_finish=models.IntegerField(null=True, blank=True, default=None)
    frequency=models.CharField(max_length=20,null=True, blank=True, default=None)


    def __str__(self):
        return f"{self.task_id},{self.name},{self.date_start},{self.date_plan},{self.date_alarm},{self.date_finish},{self.employee_id},{self.department_id},{self.leader},{self.evidence},{self.report},{self.urgent},{self.team_id},{self.team_leader},{self.manager_dep},{self.date_create},{self.date_edit},{self.note},{self.name_old},{self.date_start_old},{self.date_plan_old},{self.date_finish_old},{self.leader_old},{self.evidence_old},{self.report_old},{self.urgent_old},{self.date_edit_old},{self.email_modify},{self.infringe},{self.approvebyleader},{self.status},{self.update_progress},{self.rejectbyleader},{self.commentbyleader}"
 


class frequency_task_model(models.Model):
    
    task_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500, null=False)
    date_start=models.DateField()
    date_plan=models.DateField()
    date_finish=models.DateField(null=True,blank=True,default=None)
    employee_id=models.CharField()
    department_id=models.IntegerField(null=False,default=None)
    leader=models.CharField(null=False, default=None)
    evidence =models.ImageField(upload_to='images',null=True,blank=True,default=None)
    report=models.FileField(upload_to='files',null=True,blank=True,default=None)
    urgent=models.BooleanField(null=False,default=False)
    team_id=models.CharField(null=False, blank=False, default=None)
    team_leader=models.CharField(null=False, blank=False, default=None)
    manager_dep=models.CharField(null=False, blank=False, default=None)
    date_create=models.DateField(null=True,blank=True,default=None)
    date_edit=models.DateField(null=True,blank=True,default=None)    
    note=models.CharField(max_length=500, null=True, blank=True, default=None)
    frequency=models.CharField(null=False, blank=False, default=None)
    ip_client_create=models.CharField(null=True,blank=True,default=None)
    status=models.IntegerField(null=True, blank=True, default=None)
    date_create_weekly=models.DateField(null=True,blank=True,default=None)
    date_create_monthly=models.DateField(null=True,blank=True,default=None)
    date_create_quarterly=models.DateField(null=True,blank=True,default=None)
    date_create_yearly=models.DateField(null=True,blank=True,default=None)

    def __str__(self):
        return f"{self.task_id},{self.name},{self.date_start},{self.date_plan},{self.date_finish},{self.employee_id},{self.department_id},{self.leader},{self.evidence},{self.report},{self.urgent},{self.team_id},{self.team_leader},{self.manager_dep},{self.date_create},{self.date_edit},{self.note},{self.date_create_weekly},{self.date_create_monthly},{self.date_create_quarterly},{self.date_create_yearly}"
 