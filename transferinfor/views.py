from django.shortcuts import render,redirect, get_object_or_404
from app1.models import department as department_model
from employees.models import employee_model
from task.models import task_model 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponse, HttpResponseForbidden
import datetime
from task.views import get_client_ip
from transferinfor.forms import transformadd
from transferinfor.models import transferinfor_model
@login_required
def them_trans(request,username):
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        trans_sender=username
        employee_id=username
        date_write=datetime.date.today()        
        ip_client_create=get_client_ip(request)
        employee=employee_model.objects.get(employee_id=username)
        if request.method == "POST":
            form = transformadd(request.POST,request.FILES)
            if form.is_valid():
                trans_title=form.cleaned_data['trans_title']                
                trans_content=form.cleaned_data['trans_content']
                trans_receiver=form.cleaned_data['trans_receiver']
                trans_images=form.cleaned_data['trans_images']
                trans_report=form.cleaned_data['trans_report']
                trans_team_receiver=form.cleaned_data['trans_team_receiver']
                trans_dept_receiver=form.cleaned_data['trans_dept_receiver']
                trans_obj = transferinfor_model .objects.create(trans_sender=trans_sender,trans_title=trans_title,trans_content=trans_content,date_write=date_write,trans_receiver=trans_receiver,trans_images=trans_images,trans_report=trans_report,trans_team_receiver=trans_team_receiver,trans_dept_receiver=trans_dept_receiver, ip_client_create=ip_client_create)
                trans_obj.save()
                return redirect('/trans_sent/'+str(username))
        else:
            form = transformadd()       
    return render(request, 'them_transfer.html', {'form': form,'username':username, 'employee': employee })

@login_required
def get_trans(request,username):
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        employee=employee_model.objects.get(employee_id=username)
        trans_list=transferinfor_model.objects.filter(Q(trans_receiver__icontains=username) | Q(trans_team_receiver=None, trans_dept_receiver=employee.department_id ) |Q(trans_team_receiver=employee.team_id, trans_dept_receiver=employee.department_id )).order_by ('-transfer_id')       
        sent_trans_list= transferinfor_model.objects.filter(trans_sender=username).order_by('-transfer_id')
    return render(request,'Trans_employees.html',{'employee':employee,'trans_list':trans_list, 'username': username, 'sent_trans_list': sent_trans_list})

@login_required
def trans_sent(request,username):
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        employee=employee_model.objects.get(employee_id=username)
        trans_list=transferinfor_model.objects.filter(trans_sender=username ).order_by ('-transfer_id')       
    return render(request,'Trans_sent_employee.html',{'employee':employee,'trans_list':trans_list, 'username': username})

@login_required
def search_transfer(request,username):
    query = None
    results = []
    user =get_object_or_404(User,username=username)
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        if request.method=='GET':
            query=request.GET['Search']  # Lấy từ khóa tìm kiếm                    
            employee=employee_model.objects.get(employee_id=username)
            results = transferinfor_model.objects.filter(
        ((Q(trans_sender = query) | Q(trans_receiver = query) | Q(trans_title__icontains = query) | Q(trans_content__icontains = query)  ) & (Q(trans_sender=username) | Q(trans_receiver=username) |Q(trans_team_receiver = employee.team_id, trans_dept_receiver = employee.department_id ) |Q(trans_team_receiver = None, trans_dept_receiver = employee.department_id )))        
        ).order_by('-transfer_id')
    return render(request, 'search_trans.html', {'query': query, 'results': results, 'username' : username, 'employee':employee})