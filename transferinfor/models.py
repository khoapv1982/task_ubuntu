from django.db import models
from app1.models import department
from app1.models import team
from employees.models import employee_model

# Create your models here.
class transferinfor_model(models.Model):
    transfer_id=models.AutoField(primary_key=True)
    trans_sender=models.CharField()
    trans_title=models.CharField(max_length=500)    
    trans_content=models.CharField(max_length=1000, null=False)    
    date_write=models.DateField()    
    trans_receiver=models.CharField(null=True,blank=True,default=None)        
    trans_images =models.ImageField(upload_to='images_trans',null=True,blank=True,default=None)
    trans_report=models.FileField(upload_to='files_trans',null=True,blank=True,default=None)
    trans_team_receiver=models.CharField(null=True,blank=True,default=None)
    trans_dept_receiver=models.CharField(null=True,blank=True,default=None)        
    ip_client_create=models.CharField(null=True,blank=True,default=None)

    def __str__(self):
        return f"{self.transfer_id},{self.trans_sender},{self.trans_content},{self.date_write},{self.trans_reciever},{self.trans_images},{self.trans_report}"
 