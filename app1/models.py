from django.db import models

# Create your models here.
class department(models.Model):
    department_id= models.CharField(primary_key=True)
    name=models.CharField(max_length=50,null=False)
    manager_dep=models.CharField(null=False, blank=False, default=None)    
    def __str__(self):
        return f"{self.department_id},{self.name},{self.manager_dep}"
    
class team(models.Model):
    
    team_id= models.CharField(null=False, blank=False, default=None)
    department_id=models.CharField(null=False, blank=False, default=None)
    name=models.CharField(max_length=50,null=False)
    team_leader=models.CharField()
    manager_dep= models.CharField(null=False, blank=False, default=None)
    def __str__(self):
        return f"{self.team_id},{self.name},{self.department_id},{self.team_leader},{self.manager_dep}"
    
