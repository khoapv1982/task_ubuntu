from django.db import models
from app1.models import department
from app1.models import team

# Create your models here.
class employee_model(models.Model):
    employee_id=models.CharField(primary_key=True)
    name=models.CharField(max_length=50, null=False)    
    leader= models.CharField(null=True)
    #team_id=models.ForeignKey(team,default=None,on_delete=models.CASCADE)    
    email=models.EmailField(null=True,blank=True,default=None)
    grade=models.IntegerField(null=True,blank=True,default=None)
    team_id=models.CharField()    
    team_leader=models.CharField(null=False, blank=False, default=None)
    department_id=models.CharField()
    manager_dep=models.CharField(null=False, blank=False, default=None)
    Created_date=models.DateField(null=False, blank=False, default=None)
    # Creater=models.CharField(null=False, blank=False, default=None)
    def __str__(self):
        return f"{self.employee_id},{self.name},{self.leader},{self.team_id},{self.team_leader},{self.department_id},{self.manager_dep},{self.Created_date}"    
    # avatar =models.ImageField(upload_to='images',null=False,default=None)
    # cv=models.FileField(upload_to='files',null=False,default=None)
    
    