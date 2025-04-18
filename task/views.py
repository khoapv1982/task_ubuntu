from django.shortcuts import render,redirect, get_object_or_404
from app1.models import department as department_model, team as team_model
from employees.models import employee_model
from task.models import task_model, frequency_task_model 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import taskForm, taskFormadd, SearchForm, taskFormassign, taskFormApprove, DateFilterForm
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime
import openpyxl
from openpyxl import Workbook
from django.http import JsonResponse
import pdb
import random
from django.db.models import Count
from django.db.models import Count, Case, When, Value, IntegerField
# Danh sách màu ngẫu nhiên
current_year = datetime.now().year  
def generate_colors(n):
    return [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(n)]
@login_required
def get_chart_complete(request, username ):
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:      
        tasks = (
    task_model.objects
    .filter(
        (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username) | Q(team_leader=username)) 
        & Q(status__in=[6, 7, 8, 9]) 
        & Q(date_plan__year=current_year)
    )
    .values('employee_id')  # ✅ Gọi sau filter()
    .annotate(sl=Count('status'))  # ✅ Gọi sau values()
)
        employees = [task['employee_id'] for task in tasks]
        values = [task['sl'] for task in tasks]
        colors = generate_colors(len(employees))
        data = {"labels": employees, "values": values, "colors": colors}        
        return JsonResponse(data)
@login_required    
def get_chart_ongoing(request, username):
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:   
        tasks = task_model.objects.filter((Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)),(Q(status=3) | Q(status=4))& Q(date_plan__year=current_year)).values('employee_id').annotate(sl=Count('status'))       
        employees = [task['employee_id'] for task in tasks]
        values = [task['sl'] for task in tasks]
        colors = generate_colors(len(employees))
        data = {"labels": employees, "values": values, "colors": colors}
        return JsonResponse(data)
@login_required    
def get_chart_outofdate(request,username):
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:   
        tasks = task_model.objects.filter((Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(status=5) & Q(date_plan__year=current_year)).values('employee_id').annotate(sl=Count('status'))        
        employees = [task['employee_id'] for task in tasks]
        values = [task['sl'] for task in tasks]
        colors = generate_colors(len(employees))
        data = {"labels": employees, "values": values, "colors": colors}
        return JsonResponse(data)

# API trả về dữ liệu nhóm status
@login_required    
def get_summary_chart(request,username):
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:   
        tasks = task_model.objects.filter((Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username))& Q(date_plan__year=current_year)).annotate(
        
        status_group=Case(
            When(status=9, then=Value("Closed")),
            When(status__in=[6, 7, 8], approvebyleader=True, then=Value("Closed")), 
            When(status__in=[6, 7, 8], then=Value("Finished")),
            When(status=5, then=Value("Expired")),            
            default=Value("Open"),  # Nếu có status khác
            # output_field=IntegerField()
        )
    ).values('status_group').annotate(sl=Count('status'))
        
        
     # Định nghĩa thứ tự mong muốn của các trạng thái
    status_order = [ "Closed","Finished","Open", "Expired" ]
    color_map = {
        "Closed": "#2ECC71",    # Xanh lá
        "Finished": "#3498DB",  # Xanh dương
        "Expired": "#E74C3C",   # Đỏ
        "Open": "#F1C40F"       # Vàng
    }
     # Gán màu theo status_group, nếu không có trong color_map thì mặc định xám

       # Tạo dictionary để tra cứu số lượng
    task_dict = {task['status_group']: task['sl'] for task in tasks}
     # Sắp xếp dữ liệu theo thứ tự mong muốn
    statuses = [status for status in status_order if status in task_dict]
    values = [task_dict[status] for status in statuses]
    colors = [color_map[status] for status in statuses]
    # statuses = [task['status_group'] for task in tasks]
    # values = [task['sl'] for task in tasks]
    #colors = [color_map.get(status, "#95A5A6") for status in statuses]
    # colors = generate_colors(len(statuses))

    data = {"labels": statuses, "values": values, "colors": colors}
    return JsonResponse(data)


@login_required  
def detail_view_filter(request, category,chartID,username, start_date, end_date):
        
        if chartID =="chart1":
            data = task_model.objects.filter((Q(status=6) | Q(status=7)| Q(status=8)| Q(status=9)) & Q(employee_id=category) &(Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])).order_by('employee_id','date_plan','status')
        if chartID =="chart2":
            if category =="Finished":
                data = task_model.objects.filter((Q(status=6) | Q(status=7)| Q(status=8)) & (Q(approvebyleader =False) | Q(approvebyleader =None)) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])).order_by('employee_id','date_plan','status')
            if category =="Closed":            
                data = task_model.objects.filter((Q(status=9) | (Q(status__in=[6, 7, 8]) & Q(approvebyleader=True))) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])).order_by('employee_id','date_plan','status')
            if category =="Expired":
                data = task_model.objects.filter(Q(status=5) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])).order_by('employee_id','date_plan','status')
            if category =="Open":
                data = task_model.objects.filter((Q(status=4) | Q(status=3)) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])).order_by('employee_id','date_plan','status')
        if chartID =="chart3":
            data = task_model.objects.filter(Q(status=5) & Q(employee_id=category) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])).order_by('employee_id','date_plan','status')     
        if chartID =="chart4":
            data = task_model.objects.filter((Q(status=4) | Q(status=3)) & Q(employee_id=category) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])).order_by('employee_id','date_plan','status')
        return render(request, 'detailbk.html', {'data': data,'chartID': chartID,'category' : category,'username': username,})

@login_required
def get_task(request,username):    
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        form= DateFilterForm    
        team_list= team_model.objects.filter(manager_dep = username).order_by('team_id')    
        task_list=task_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username)),date_finish=None).order_by('employee_id','-urgent','-status','date_plan','date_start' )
        employee=employee_model.objects.get(employee_id=username)
        employee_list=employee_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id')
        return render(request,'task_employee_2.html',{'task_list':task_list,'employee':employee,'employee_list':employee_list,'username': username, 'form': form, 'team_list': team_list},)


@login_required
def update_task(request,username, id):
    user =get_object_or_404(User,username=username)     
    if request.user != user :
       return HttpResponse('You have not permission to access this page')
    else:        
        task_obj = task_model.objects.get(task_id=id, date_finish=None,)
        if task_obj.employee_id == username:
            task_obj.name_old=task_obj.name
            task_obj.date_start_old=task_obj.date_start
            task_obj.date_plan_old=task_obj.date_plan
            task_obj.date_finish_old=task_obj.date_finish
            task_obj.evidence_old=task_obj.evidence
            task_obj.report_old=task_obj.report
            task_obj.urgent_old=task_obj.urgent
            task_obj.ip_client_edit_old=task_obj.ip_client_edit
            task_obj.date_edit_old=task_obj.date_edit        
            task_obj.save() 
            employee_obj= employee_model.objects.get(employee_id=username) 
            if request.method == "POST":
                form = taskForm(request.POST,request.FILES)
                if form.is_valid():
                    task_obj.date_finish=form.cleaned_data['date_finish']
                    task_obj.evidence=form.cleaned_data['evidence']
                    task_obj.report=form.cleaned_data['report']
                    task_obj.date_edit=datetime.today()
                    task_obj.ip_client_edit=get_client_ip(request)
                    task_obj.name=form.cleaned_data['name']
                    task_obj.date_start=form.cleaned_data['date_start']
                    task_obj.date_plan=form.cleaned_data['date_plan']    
                    task_obj.update_progress=form.cleaned_data['update_progress']    
                    if (task_obj.date_finish != None) and (task_obj.date_finish<  task_obj.date_start):
                        return JsonResponse({"error": "Ngay hoan thanh khong duoc truoc ngay bat dau"}, status=400)
                    if (task_obj.date_finish != task_obj.date_finish_old) and (task_obj.date_finish != None) :
                        task_obj.email_finish=0
                        if task_obj.date_finish > task_obj.date_plan:
                            task_obj.status=6 
                        else:
                            task_obj.status=7
                    else:                        
                        task_obj.email_modify=0      
                    task_obj.save()
                    return redirect('/task/'+str(username))
            else:
                form = taskForm(instance=task_obj)
                return render(request, 'update_task.html', {'form': form,'task_obj':task_obj, 'employee_id': username, 'username': username, 'employee': employee_obj})
    

@login_required
def them_task(request,username):
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        task_list=task_model.objects.filter(employee_id=username).order_by('-task_id' )
        employee_obj= employee_model.objects.get(employee_id=username)    
        employee_id=username
        department_id=employee_obj.department_id
        leader=employee_obj.leader
        team_id=employee_obj.team_id
        team_leader=employee_obj.team_leader
        manager_dep=employee_obj.manager_dep  
        date_create=datetime.today()
        ip_client_create=get_client_ip(request)

        if request.method == "POST":
            form = taskFormadd(request.POST,request.FILES)
            if form.is_valid():
                name=form.cleaned_data['name']
                date_start=form.cleaned_data['date_start']
                date_plan=form.cleaned_data['date_plan']
                date_alarm=form.cleaned_data['date_alarm']
                urgent=form.cleaned_data['urgent']
                evidence=form.cleaned_data['evidence']
                report=form.cleaned_data['report']
                status=4
                task_obj = task_model.objects.create(employee_id=employee_id,department_id=department_id,leader=leader,team_id=team_id,team_leader=team_leader,manager_dep=manager_dep,name=name,date_start=date_start,date_plan=date_plan,date_alarm=date_alarm,urgent=urgent,evidence=evidence, report=report,date_create=date_create, ip_client_create=ip_client_create,status=status)
                task_obj.save()
                if form.cleaned_data['checkbox_1']==True:
                    frequency= "Weekly"
                    task_frequency_obj = frequency_task_model.objects.create(employee_id=employee_id,department_id=department_id,leader=leader,team_id=team_id,team_leader=team_leader,manager_dep=manager_dep,name=name,date_start=date_start,date_plan=date_plan,urgent=urgent,evidence=evidence, report=report,date_create=date_create, ip_client_create=ip_client_create, frequency=frequency,status=4,date_create_weekly=date_create )
                    task_frequency_obj.save()
                elif form.cleaned_data['checkbox_2']==True:
                    frequency= "Monthly"
                    task_frequency_obj = frequency_task_model.objects.create(employee_id=employee_id,department_id=department_id,leader=leader,team_id=team_id,team_leader=team_leader,manager_dep=manager_dep,name=name,date_start=date_start,date_plan=date_plan,urgent=urgent,evidence=evidence, report=report,date_create=date_create, ip_client_create=ip_client_create, frequency=frequency,status=4,date_create_monthly=date_create)
                    task_frequency_obj.save()
                elif form.cleaned_data['checkbox_3']==True:
                    frequency= "Quarterly"
                    task_frequency_obj = frequency_task_model.objects.create(employee_id=employee_id,department_id=department_id,leader=leader,team_id=team_id,team_leader=team_leader,manager_dep=manager_dep,name=name,date_start=date_start,date_plan=date_plan,urgent=urgent,evidence=evidence, report=report,date_create=date_create, ip_client_create=ip_client_create, frequency=frequency,status=4,date_create_quarterly=date_create)
                    task_frequency_obj.save()
                elif form.cleaned_data['checkbox_4']==True:
                    frequency= "Yearly"    
                    task_frequency_obj = frequency_task_model.objects.create(employee_id=employee_id,department_id=department_id,leader=leader,team_id=team_id,team_leader=team_leader,manager_dep=manager_dep,name=name,date_start=date_start,date_plan=date_plan,urgent=urgent,evidence=evidence, report=report,date_create=date_create, ip_client_create=ip_client_create, frequency=frequency,status=4,date_create_yearly=date_create)
                    task_frequency_obj.save()                
            return redirect('/task/'+str(username))
        else:
            form = taskFormadd(initial={'employee_id':employee_id,'department_id':department_id,'leader':leader,'team_id':team_id,'team_leader':team_leader,'manager_dep':manager_dep})       
    return render(request, 'them_task.html', {'form': form,'username':username, 'employee': employee_obj, 'task_list':task_list })
def get_error(request):    
    return render(request,'error.html')


@login_required
def get_task_detail(request,username,employee_id):    
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        task_list=task_model.objects.filter(employee_id=employee_id).order_by('date_start','date_plan' )
        employee=employee_model.objects.get(employee_id=employee_id)        
    return render(request,'task_detail.html',{'task_list':task_list,'username':username,'employee':employee})

def search_new(request,username):
    query = None
    results = []
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        if request.method=='GET':
            query=request.GET['Search']  # Lấy từ khóa tìm kiếm                    
            results = task_model.objects.filter(
        (Q(name__icontains = query) & (Q(employee_id=username) | Q(leader=username) | Q(team_leader = username)| Q(manager_dep = username)))
        | (Q(employee_id__icontains = query) & (Q(employee_id=username) | Q(leader=username) | Q(team_leader = username)| Q(manager_dep = username)))    
        ).order_by('employee_id','-date_finish','-date_start')
    return render(request, 'search_new.html', {'query': query, 'results': results, 'username' : username})

def get_client_ip(request):
    # Kiểm tra nếu có sử dụng proxy hoặc load balancer
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Trong trường hợp có nhiều IP, lấy IP đầu tiên
    else:
        ip = request.META.get('REMOTE_ADDR')  # Lấy IP từ 'REMOTE_ADDR'
    
    return ip
@login_required
def them_assign(request,username):
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')   
    else:
        employee = employee_model.objects.get(employee_id=username) 
        date_write=datetime.today()        
        ip_client_create=get_client_ip(request)
                
        if request.method == "POST":
            form = taskFormassign(request.POST,request.FILES)
            if form.is_valid():
                name=form.cleaned_data['name']                
                urgent=form.cleaned_data['urgent']
                date_start=form.cleaned_data['date_start']
                date_plan=form.cleaned_data['date_plan']
                date_alarm=form.cleaned_data['date_alarm']
                evidence=form.cleaned_data['evidence']
                report=form.cleaned_data['report']
                employee_id=form.cleaned_data['employee_id']
                if not (employee_model.objects.filter((Q(leader=username) | Q(team_leader=username) | Q(manager_dep=username)),employee_id=employee_id).exists()):
                    return HttpResponse('You have not permission to assign task to this employee')
                else:
                    leader=username                    
                    employee_obj=employee_model.objects.get(employee_id=employee_id)
                    team_id=employee_obj.team_id
                    team_leader=employee_obj.team_leader
                    department_id=employee_obj.department_id
                    manager_dep=employee_obj.manager_dep
                    task_obj = task_model.objects.create(employee_id=employee_id,name=name,urgent=urgent,date_start=date_start, date_plan=date_plan, date_alarm=date_alarm, evidence=evidence, report=report,leader=leader, team_id=team_id, team_leader=team_leader, department_id=department_id, manager_dep=manager_dep, date_create=date_write, ip_client_create=ip_client_create, note="Assigned")
                    task_obj.save()                      
                    return redirect('/task/'+str(username))
        else:
            form = taskFormassign()       
    return render(request, 'them_assign_task.html', {'form': form,'username':username, 'employee': employee })
@login_required
def search_assign(request,username):
    query = None
    results = []
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        if request.method=='GET':
            query=request.GET['Search']  # Lấy từ khóa tìm kiếm                    
            results = task_model.objects.filter(
        (Q(name__icontains = query) & (Q(leader=username)) & (Q(note="Assigned")) )
        | (Q(employee_id__icontains = query) & (Q(leader=username)) & (Q(note="Assigned")) )).order_by('-task_id')
    return render(request, 'search_assign.html', {'query': query, 'results': results, 'username' : username})
@login_required
def export_task_employee(request, username, employee_id ):
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        # Tạo Workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Personal_task"

        # Thêm header
        headers = ['task_id', 'name', 'date_start', 'date_plan','date_finish','employee_id','department_id','leader','evidence','report','urgent','team_id','team_leader','manager_dep','date_create','date_edit','note']
        sheet.append(headers)

        # Lấy dữ liệu từ database
        tasks = task_model.objects.filter(employee_id=employee_id).values_list('task_id', 'name', 'date_start', 'date_plan','date_finish','employee_id','department_id','leader','evidence','report','urgent','team_id','team_leader','manager_dep','date_create','date_edit','note').order_by('-task_id')
        for task in tasks:
            sheet.append(task)

        # Tạo response với file Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=personal_task.xlsx'
        workbook.save(response)

    return response
def search_employee(request):
    query = request.GET.get("q", "")
    employees = employee_model.objects.filter(name__icontains=query).order_by("name")[:5]
    data = [{"employee_id": emp.employee_id, "name": emp.name} for emp in employees]    
    return JsonResponse(data, safe=False)





@login_required
def approve_task_done(request,username, id):
    user =get_object_or_404(User,username=username)     
    if request.user != user :
       return HttpResponse('You have not permission to access this page')
    else:
        
        task_obj = task_model.objects.get(task_id=id)
        if task_obj.leader == username:
            form= taskFormApprove
            employee_obj= employee_model.objects.get(employee_id=username) 
            if request.method == "POST":
                form = taskFormApprove(request.POST,request.FILES)
                if form.is_valid():
                    task_obj.approvebyleader=form.cleaned_data['approvebyleader']
                    task_obj.rejectbyleader=form.cleaned_data['rejectbyleader']
                    task_obj.commentbyleader=form.cleaned_data['commentbyleader']                                       
                    task_obj.ip_client_edit=get_client_ip(request)                     
                    task_obj.email_approve=0  
                    if task_obj.rejectbyleader==True:
                        task_obj.approvebyleader=False
                        task_obj.date_finish=None    
                        task_obj.date_reject=datetime.today()    
                    if task_obj.approvebyleader==True:
                        task_obj.rejectbyleader=False
                        task_obj.status=9
                        task_obj.date_approved=datetime.today()                        
                    task_obj.save()
                    return redirect('/approvetasklist/'+str(username))                
            else:
                form = taskFormApprove(instance=task_obj)
        return render(request, 'approve_task_done.html', {'form': form,'task_obj':task_obj, 'employee_id': username, 'username': username, 'employee': employee_obj})
@login_required
def approve_task_list(request,username):
    user =get_object_or_404(User,username=username)     
    if request.user != user :
       return HttpResponse('You have not permission to access this page')
    else:
        
        # task_obj = task_model.objects.get(leader=username, date_finish__isnull=False,approvebyleader__isnull=False,rejectbyleader__isnull=False).order_by('employee_id')
        # task_obj = task_model.objects.filter().order_by('employee_id')
        # return render(request, 'approve_task_list.html', {'task_obj': task_obj, 'employee_id': username, 'username': username,})

        task_list=task_model.objects.filter(Q(leader = username,date_finish__isnull=False, approvebyleader__isnull=True) | Q(leader = username,date_finish__isnull=False, approvebyleader=False) ).order_by('employee_id' )
        employee=employee_model.objects.get(employee_id=username)
        employee_list=employee_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id')
        return render(request,'approve_task_list.html',{'task_list':task_list,'employee':employee,'employee_list':employee_list,'username': username})
def bulk_update_approved(request,username):
    user =get_object_or_404(User,username=username)     
    if request.user != user :
       return HttpResponse('You have not permission to access this page')
    else:
        if request.method == "POST":
            task_ids = request.POST.getlist("task_checkbox")  # Lấy danh sách ID của task được chọn

            # Cập nhật trạng thái `approved` cho các task được chọn
            task_model.objects.filter(task_id__in=task_ids).update(approvebyleader=True,date_approved= datetime.today(),rejectbyleader=False,email_approve=0,commentbyleader='bulk_approved' )                        
            return redirect('/approvetasklist/'+str(username))      
@login_required
def approved(request,username):
    user =get_object_or_404(User,username=username)     
    if request.user != user :
       return HttpResponse('You have not permission to access this page')
    else:
        task_list=task_model.objects.filter((Q(employee_id=username) | Q(leader = username)),approvebyleader=True).order_by('employee_id' )
        employee=employee_model.objects.get(employee_id=username)
        employee_list=employee_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id')
        return render(request,'approved.html',{'task_list':task_list,'employee':employee,'employee_list':employee_list,'username': username})
@login_required
def outofdate_task(request,username):
    user =get_object_or_404(User,username=username)     
    if request.user != user :
       return HttpResponse('You have not permission to access this page')
    else:
        task_list=task_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username)),(Q(status=6) | Q(status=5))).order_by('employee_id','status','date_plan' )
        employee=employee_model.objects.get(employee_id=username)
        employee_list=employee_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id')
        return render(request,'outofdate_task.html',{'task_list':task_list,'employee':employee,'employee_list':employee_list,'username': username})
@login_required
def task_done(request,username):    
    user =get_object_or_404(User,username=username)     
    if request.user != user :
       return HttpResponse('You have not permission to access this page')
    else:
        task_list=task_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username)),date_finish__isnull=False ).order_by('employee_id','status' )
        employee=employee_model.objects.get(employee_id=username)
        employee_list=employee_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id')
        return render(request,'task_done.html',{'task_list':task_list,'employee':employee,'employee_list':employee_list,'username': username})



def filter_tasks(request, username, start_date, end_date, status_list):
    user = get_object_or_404(User, username=username)

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)

    if end_date < start_date:
        return JsonResponse({"error": "End date cannot be earlier than start date"}, status=400)

    tasks = (
        task_model.objects.filter(
            (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username) | Q(team_leader=username))
            & Q(status__in=status_list)
            & Q(date_plan__range=[start_date, end_date])
        )
        .values("employee_id")
        .annotate(sl=Count("status"))
    )

    employees = [task["employee_id"] for task in tasks]
    values = [task["sl"] for task in tasks]
    colors = generate_colors(len(employees))
    data = {"labels": employees, "values": values, "colors": colors}        
    return JsonResponse(data)

# Các API riêng biệt cho từng trạng thái công việc
def complete_data_filterdate(request, username, start_date, end_date):
    return filter_tasks(request, username, start_date, end_date, [6, 7, 8, 9])

def ongoing_data_filterdate(request, username, start_date, end_date):
    return filter_tasks(request, username, start_date, end_date, [3, 4])

def expiredate_data_filterdate(request, username, start_date, end_date):
    return filter_tasks(request, username, start_date, end_date, [5])

def get_summary_chart_filter(request,username, start_date, end_date):
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:   
        tasks = task_model.objects.filter((Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username))& Q(date_plan__range=[start_date, end_date])).annotate(
        
        status_group=Case(
            When(status=9, then=Value("Closed")),
            When(status__in=[6, 7, 8], approvebyleader=True, then=Value("Closed")), 
            When(status__in=[6, 7, 8], then=Value("Finished")),
            When(status=5, then=Value("Expired")),            
            default=Value("Open"),  # Nếu có status khác
            # output_field=IntegerField()
        )
    ).values('status_group').annotate(sl=Count('status'))
        
        
     # Định nghĩa thứ tự mong muốn của các trạng thái
    status_order = [ "Closed","Finished","Open", "Expired" ]
    color_map = {
        "Closed": "#2ECC71",    # Xanh lá
        "Finished": "#3498DB",  # Xanh dương
        "Expired": "#E74C3C",   # Đỏ
        "Open": "#F1C40F"       # Vàng
    }
     # Gán màu theo status_group, nếu không có trong color_map thì mặc định xám

       # Tạo dictionary để tra cứu số lượng
    task_dict = {task['status_group']: task['sl'] for task in tasks}
     # Sắp xếp dữ liệu theo thứ tự mong muốn
    statuses = [status for status in status_order if status in task_dict]
    values = [task_dict[status] for status in statuses]
    colors = [color_map[status] for status in statuses]
    # statuses = [task['status_group'] for task in tasks]
    # values = [task['sl'] for task in tasks]
    #colors = [color_map.get(status, "#95A5A6") for status in statuses]
    # colors = generate_colors(len(statuses))

    data = {"labels": statuses, "values": values, "colors": colors}
    return JsonResponse(data)

def filter_tasks_team(request, username, start_date, end_date, status_list,team_id):
    user = get_object_or_404(User, username=username)

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)

    if end_date < start_date:
        return JsonResponse({"error": "End date cannot be earlier than start date"}, status=400)

    tasks = (
        task_model.objects.filter(
            (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username) | Q(team_leader=username))
            & Q(status__in=status_list)
            & Q(date_plan__range=[start_date, end_date])
            & Q(team_id=team_id)    
        )
        .values("employee_id")
        .annotate(sl=Count("status"))
    )

    employees = [task["employee_id"] for task in tasks]
    values = [task["sl"] for task in tasks]
    colors = generate_colors(len(employees))
    data = {"labels": employees, "values": values, "colors": colors}        
    return JsonResponse(data)

# Các API riêng biệt cho từng trạng thái công việc
def complete_data_filterdate_team(request, username, start_date, end_date,team_id):
    return filter_tasks_team(request, username, start_date, end_date, [6, 7, 8, 9],team_id)

def ongoing_data_filterdate_team(request, username, start_date, end_date,team_id):
    return filter_tasks_team(request, username, start_date, end_date, [3, 4],team_id)

def expiredate_data_filterdate_team(request, username, start_date, end_date,team_id):
    return filter_tasks_team(request, username, start_date, end_date, [5],team_id)

def get_summary_chart_filter_team(request,username, start_date, end_date,team_id):
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:   
        tasks = task_model.objects.filter((Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username))& Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).annotate(
        
        status_group=Case(
            When(status=9, then=Value("Closed")),
            When(status__in=[6, 7, 8], approvebyleader=True, then=Value("Closed")), 
            When(status__in=[6, 7, 8], then=Value("Finished")),
            When(status=5, then=Value("Expired")),            
            default=Value("Open"),  # Nếu có status khác
            # output_field=IntegerField()
        )
    ).values('status_group').annotate(sl=Count('status'))
        
        
     # Định nghĩa thứ tự mong muốn của các trạng thái
    status_order = [ "Closed","Finished","Open", "Expired" ]
    color_map = {
        "Closed": "#2ECC71",    # Xanh lá
        "Finished": "#3498DB",  # Xanh dương
        "Expired": "#E74C3C",   # Đỏ
        "Open": "#F1C40F"       # Vàng
    }
     # Gán màu theo status_group, nếu không có trong color_map thì mặc định xám

       # Tạo dictionary để tra cứu số lượng
    task_dict = {task['status_group']: task['sl'] for task in tasks}
     # Sắp xếp dữ liệu theo thứ tự mong muốn
    statuses = [status for status in status_order if status in task_dict]
    values = [task_dict[status] for status in statuses]
    colors = [color_map[status] for status in statuses]
    # statuses = [task['status_group'] for task in tasks]
    # values = [task['sl'] for task in tasks]
    #colors = [color_map.get(status, "#95A5A6") for status in statuses]
    # colors = generate_colors(len(statuses))

    data = {"labels": statuses, "values": values, "colors": colors}
    return JsonResponse(data)

@login_required  
def detail_view_filter_team(request, category,chartID,username, start_date, end_date,team_id):
        
        if chartID =="chart1":
            data = task_model.objects.filter((Q(status=6) | Q(status=7)| Q(status=8)| Q(status=9)) & Q(employee_id=category) &(Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).order_by('employee_id','date_plan','status')
        if chartID =="chart2":
            if category =="Finished":
                data = task_model.objects.filter((Q(status=6) | Q(status=7)| Q(status=8)) & (Q(approvebyleader =False) | Q(approvebyleader =None)) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).order_by('employee_id','date_plan','status')
            if category =="Closed":            
                data = task_model.objects.filter((Q(status=9) | (Q(status__in=[6, 7, 8]) & Q(approvebyleader=True))) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).order_by('employee_id','date_plan','status')
            if category =="Expired":
                data = task_model.objects.filter(Q(status=5) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).order_by('employee_id','date_plan','status')
            if category =="Open":
                data = task_model.objects.filter((Q(status=4) | Q(status=3)) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).order_by('employee_id','date_plan','status')
        if chartID =="chart3":
            data = task_model.objects.filter(Q(status=5) & Q(employee_id=category) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).order_by('employee_id','date_plan','status')     
        if chartID =="chart4":
            data = task_model.objects.filter((Q(status=4) | Q(status=3)) & Q(employee_id=category) & (Q(employee_id=username) | Q(leader=username) | Q(manager_dep=username)| Q(team_leader=username)) & Q(date_plan__range=[start_date, end_date])& Q(team_id=team_id)).order_by('employee_id','date_plan','status')
        return render(request, 'detailbk.html', {'data': data,'chartID': chartID,'category' : category,'username': username,})

@login_required
def get_task_frequency(request,username):    
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:                
        task_f_list= frequency_task_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id','-task_id' )
        employee=employee_model.objects.get(employee_id=username)
        employee_list=employee_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id')
        return render(request,'frequency_employee.html',{'task_f_list':task_f_list,'employee':employee,'employee_list':employee_list,'username': username},)

@login_required
def delete_task_f(request,username, id):    
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:                
        task_f_obj = frequency_task_model.objects.filter(employee_id=username, task_id=id).delete()
        task_f_list= frequency_task_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id','-task_id' )
        employee=employee_model.objects.get(employee_id=username)
        employee_list=employee_model.objects.filter((Q(employee_id=username) | Q(leader = username)| Q(team_leader = username)| Q(manager_dep = username))).order_by('employee_id')
        return render(request,'frequency_employee.html',{'task_f_list':task_f_list,'employee':employee,'employee_list':employee_list,'username': username},)
    

    

