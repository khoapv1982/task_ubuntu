from django.contrib import admin
from .models import employee_model

# Register your models here.
class employeeAdmin(admin.ModelAdmin):
    list_display=('employee_id','department_id','name','leader')
    search_fields=['name']
    list_filter=('employee_id','department_id','name')

admin.site.register(employee_model,employeeAdmin)
