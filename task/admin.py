from django.contrib import admin
from .models import task_model, frequency_task_model

# Register your models here.
class taskAdmin(admin.ModelAdmin):
    list_display=('task_id','name','date_start','date_plan','date_finish','employee_id','department_id','leader','evidence','report','urgent')
    search_fields=['name']
    list_filter=('employee_id','name','urgent')

class taskfrequency(admin.ModelAdmin):
    list_display=('task_id','name','date_start','date_plan','date_finish','employee_id','department_id','leader','evidence','report','urgent','frequency')
    search_fields=['name']
    list_filter=('employee_id','name','frequency')

admin.site.register(task_model,taskAdmin)
admin.site.register(frequency_task_model,taskfrequency)