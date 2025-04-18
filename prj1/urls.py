
from django.contrib import admin
from django.urls import path
from app1 import views
from employees import views as employees_views
from task.views import (get_task, update_task, them_task,get_error,get_task_detail, search_new, them_assign, search_assign, 
                        export_task_employee,search_employee, approve_task_list, approve_task_done,bulk_update_approved, approved, outofdate_task, 
                        task_done, get_chart_complete,get_chart_ongoing,get_chart_outofdate, get_summary_chart, complete_data_filterdate, 
                        ongoing_data_filterdate, expiredate_data_filterdate, get_summary_chart_filter,detail_view_filter,
                        complete_data_filterdate_team,ongoing_data_filterdate_team, expiredate_data_filterdate_team, get_summary_chart_filter_team,detail_view_filter_team,
                        get_task_frequency,delete_task_f)

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from transferinfor.views import them_trans, get_trans, search_transfer,trans_sent
urlpatterns = [
    path('admin/', admin.site.urls),
    path('deptlist/<str:username>/', views.gethome),        
    path('adddept/<str:username>/', views.add_department),
    path('addteam/<str:username>/', views.add_team),
    path('department/<str:username>/<str:id>/',employees_views.get_employees),            
    path('upload_excel/<str:username>/',views.upload_excel,name='upload_excel'),
    path('upload_excel_emp/<str:username>/',employees_views.upload_excel_emp,name='upload_excel_emp'),        
    path('',views.login_view2,name='login2'),
    path('login/',views.login_view2,name='login2'),    
    path('task/<str:username>/',get_task,name='task_employee'),
    path('logout/',views.CustomLogoutView.as_view(),name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),    
    path('addtaskForm/<str:username>',them_task),    
    path('update_task/<str:username>/<int:id>/', update_task, name='update_task'),  
    path('detailtask/<str:username>/<str:employee_id>/', get_task_detail, name='detail_task'),  
    path('search/<str:username>/', search_new, name='search_new'),
    path('error/', get_error, name='error_page'), 
    path('addtrans/<str:username>',them_trans),
    path('gettrans/<str:username>',get_trans,name='trans_employee'),
    path('trans_sent/<str:username>',trans_sent,name='trans_sent_employee'),
    path('search/<str:username>/transfer', search_transfer, name='search_transfer'),
    path('addtaskassign/<str:username>',them_assign),
    path('search/<str:username>/assign', search_assign, name='search_assign' ),
    path('export-employees/', employees_views.export_employees_to_excel, name='export_employees'),
    path('exporttask/<str:username>/<str:employee_id>/',export_task_employee,name='export_task_employee'),
    path("searchnv/", search_employee, name="search_employee"),
    path("searchphong/", views.search_phong, name="search_phong"),
    path('approvetasklist/<str:username>',approve_task_list,name="approve_task_list"),
    path('approvetaskdone/<str:username>/<int:id>/', approve_task_done, name='approve_task_done'), 
    path("update-approved/<str:username>", bulk_update_approved, name="bulk_update_approved"),
    path('approved/<str:username>',approved,name="approved"),
    path('outofdate_task/<str:username>',outofdate_task,name="outofdate_task"),
    path('task_done/<str:username>',task_done,name="outofdate_task"),    
    path('chart_complete/<str:username>/',get_chart_complete,name="chart-complete"),
    path('chart_ongoing/<str:username>/',get_chart_ongoing,name="chart-ongoing"),
    path('chart_outofdate/<str:username>/',get_chart_outofdate,name="chart-outofdate"),
    path('chart_summary/<str:username>/',get_summary_chart,name="chart-summary"),          
    path('complete/<str:username>/<str:start_date>/<str:end_date>/', complete_data_filterdate, name='complete_data_filterdate'),
    path('ongoing/<str:username>/<str:start_date>/<str:end_date>/', ongoing_data_filterdate, name='ongoing_data_filterdate'),
    path('expired/<str:username>/<str:start_date>/<str:end_date>/', expiredate_data_filterdate, name='expiredate_data_filterdate'),
    path('summary/<str:username>/<str:start_date>/<str:end_date>/', get_summary_chart_filter, name='get_summary_chart_filter'),         
    path('detail/<str:category>/<str:chartID>/<str:username>/<str:start_date>/<str:end_date>/',detail_view_filter,name="detail_view_filter"),

    path('complete/<str:username>/<str:start_date>/<str:end_date>/<str:team_id>/', complete_data_filterdate_team, name='complete_data_filterdate_team'),
    path('ongoing/<str:username>/<str:start_date>/<str:end_date>/<str:team_id>/', ongoing_data_filterdate_team, name='ongoing_data_filterdate_team'),
    path('expired/<str:username>/<str:start_date>/<str:end_date>/<str:team_id>/', expiredate_data_filterdate_team, name='expiredate_data_filterdate_team'),
    path('summary/<str:username>/<str:start_date>/<str:end_date>/<str:team_id>/', get_summary_chart_filter_team, name='get_summary_chart_filter_team'),         
    path('detail/<str:category>/<str:chartID>/<str:username>/<str:start_date>/<str:end_date>/<str:team_id>/',detail_view_filter_team,name="detail_view_filter_team"),
    path('taskfrequency/<str:username>',get_task_frequency,name="get_task_frequency"),  
    path('delete_task_f/<str:username>/<int:id>/', delete_task_f, name='delete_task_f'),  
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header='SEEV'
