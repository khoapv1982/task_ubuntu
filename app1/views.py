from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import department as department_model, team as team_model
from employees.models import employee_model
from .forms import department_form, team_form
from .forms import employee_form
from .forms import LoginForm
import openpyxl
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse

# Create your views here.
def search_phong(request):
    query = request.GET.get("q", "")
    departments = department_model.objects.filter(name__icontains=query).order_by("name")[:5]
    data = [{"department_id": department.department_id, "name": department.name, "manager_dep": department.manager_dep, } for department in departments]
    return JsonResponse(data, safe=False)
def search_team(request):
    query = request.GET.get("q", "")
    teams = team_model.objects.filter(team_id__icontains=query).order_by("team_id")[:5]
    data = [{"team_id": team.team_id, "name": team.name} for team in teams]
    return JsonResponse(data, safe=False)
def search_employee(request):
    query = request.GET.get("q", "")
    employees = employee_model.objects.filter(name__icontains=query).order_by("name")[:5]
    data = [{"employee_id": emp.employee_id, "name": emp.name} for emp in employees]    
    return JsonResponse(data, safe=False)
@login_required
def gethome(request,username):
    user =get_object_or_404(User,username=username)    
    if request.user != user :
        return HttpResponse('You have not permission to access this page')
    else:
        department_list= department_model.objects.filter().order_by('department_id')
        employee= employee_model.objects.get(employee_id=username)

    return render(request,'home.html',{'department_list':department_list,'username': username, 'employee': employee})
@login_required
def add_department(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.user != user or not user.is_superuser :
        return HttpResponse('You have not permission to access this page')
    
    if request.method == 'POST':
        form = department_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/deptlist/'+str(username))
        else:
            return render(request, 'add_department2.html', {'form': form})
    
    # 👉 Trường hợp GET: hiển thị form trống để thêm department
    else:
        form = department_form()
        return render(request, 'add_department2.html', {'form': form})

@login_required
def add_team(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.user != user or not user.is_superuser :
        return HttpResponse('You have not permission to access this page')
    
    if request.method == 'POST':
        form = team_form(request.POST)
        if form.is_valid():
            department_id = form.cleaned_data['department_id']
            manager_dep = form.cleaned_data['manager_dep']  
            team_id = form.cleaned_data['team_id'] 
            name = form.cleaned_data['name']
            team_leader = form.cleaned_data['team_leader']
            if not team_model.objects.filter(team_id=team_id, department_id=department_id).exists():
                team_model.objects.create(name=name,team_id=team_id,team_leader=team_leader,department_id=department_id,manager_dep=manager_dep)
            else:   
                return HttpResponse('Team you create is already exist.')             
                
            return redirect('/deptlist/'+str(username))
        else:
            return render(request, 'add_team.html', {'form': form})
    
    # 👉 Trường hợp GET: hiển thị form trống để thêm department
    else:
        form = team_form()
        return render(request, 'add_team.html', {'form': form})
    
def add_employee(request):
    if request.method=='POST':
        form=employee_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/department/'+str(form.cleaned_data['department_id'])[:str(form.cleaned_data['department_id']).find(',')])
        
    else:
        form=employee_form()
    return render(request,'add_employee.html',{'form':form})
@login_required    
def upload_excel(request,username):
    user =get_object_or_404(User,username=username)    
    if request.user != user or not user.is_superuser :
        return HttpResponse('You have not permission to access this page')
    else:     
        if request.method == 'POST' and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            upload_file_url = fs.url(filename)
            wb = openpyxl.load_workbook(fs.path(filename))
            sheet = wb.active
            for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                username1, email, password, is_staff = row
                if username1 is None:
                    messages.error(request, f"Dòng {index}: Thiếu username.")
                    continue
                username1 = str(username1).strip()
                email = str(email).strip() if email else ""
                password = str(password).strip() if password else "default_password"
                is_staff = bool(is_staff)

                if not username1:
                    messages.error(request, f"Dòng {index}: Username rỗng.")
                    continue

                if not User.objects.filter(username=username1).exists():
                    try:
                        User.objects.create_user(
                            username=username1,
                            email=email,
                            password=password,
                            is_staff=is_staff
                        )
                    except Exception as e:
                        messages.error(request, f"Dòng {index}: Lỗi tạo user {username1} - {e}")
                else:
                    messages.warning(request, f"Dòng {index}: Username {username1} đã tồn tại.")

            return redirect('upload_excel',username=username)  # ✅ đảm bảo trả về sau khi xử lý
        # return HttpResponse('Finish upload user list')
    # ✅ đảm bảo có return nếu không phải POST hoặc không có file
        return render(request, 'upload_excel.html')


def login_view2(request):
    if request.method=='POST':        
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(request,username=username,password=password)
        if user is not None:
                login(request,user)
                return redirect(f'/task/{username}/')
        else:
                #return render(request,'error.html')  
                thongbao="Please check your username and password"
                return render(request,'login_2.html',{'thongbao': thongbao})
    else:    
        thongbao=""    
        return render(request,'login_2.html')


class CustomLogoutView(LogoutView):
    next_page='/login/'



    
