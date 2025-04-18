from django.contrib import admin
from .models import department,team
# Register your models here.
class departmentAdmin(admin.ModelAdmin):
    list_display=('department_id','name')
    search_fields=['name']
    list_filter=('department_id','name')
admin.site.register(department,departmentAdmin)


class teamAdmin(admin.ModelAdmin):
    list_display=('team_id','department_id','name','team_leader','manager_dep')
    search_fields=['name']
    list_filter=('team_id','department_id','name','team_leader','manager_dep')
admin.site.register(team,teamAdmin)
