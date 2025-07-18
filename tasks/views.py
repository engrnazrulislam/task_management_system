from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib.auth.models import User
from users.views import is_admin
# Create your views here.

def is_Manager(user):
    return user.groups.filter(name='Manager').exists()

def is_Employee(user):
    return user.groups.filter(name='Employee').exists()


def dashboard(request):
    return render(request,'dashboard/dashboard.html')

@user_passes_test(is_Manager, login_url='no_permission')
def manager_dashboard(request):
    tasks = Task.objects.select_related('taskDetails').prefetch_related('assigned_to').all()
    # Getting task count
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed = Count('id', filter=Q(status="COMPLETED")),
        in_progress = Count('id',filter=Q(status = "IN_PROGRESS")),
        pending = Count('id', filter=Q(status="PENDING"))
    )
    
    # Retrieve Data based on criteria

    # get data from the url
    type = request.GET.get('type','all')

    # base query
    base_query = Task.objects.select_related('taskDetails').prefetch_related('assigned_to')

    #condition to retrieve data by url type
    if type == "completed":
        tasks = base_query.filter(status="COMPLETED")
    elif type == "in_progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type == "pending":
        tasks = base_query.filter(status="PENDING")
    elif type == "all" :
        base_query.all()

    # print(tasks)

    context ={
        "tasks": tasks,
        "counts": counts
    }
    
    return render(request,'dashboard/manager_dashboard.html',context)

# CRUD
# C=CREATE
# R = READ
# U = UPDATE
# D = DELETE

@user_passes_test(is_Employee, login_url='no_permission')
def employee_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

@login_required
@permission_required('tasks.add_task', login_url = 'no_permission')
def create_task(request):
    employees=User.objects.all()
    task_form = TaskModelForm() # For GET
    task_detail_form = TaskDetailModelForm() # GET operation

    if request.method == 'POST':
        # form = TaskForm(request.POST, employees=employees) # For Django Basic Form POST
        task_form = TaskModelForm(request.POST) # For Django Model Form
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ For Django Model Form """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request,'Task Created Successfully')
            return redirect('create_task')
            # return render(request, 'test_form.html', {"task_form":task_form,"task_detail_form":task_detail_form,"message":"Data is successfully added"})
            """ For Django Basic Form  Data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task=Task.objects.create(title=title, description=description, due_date=due_date)

            # # Assign employee to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            
            # return HttpResponse('Task Added Successfully')

    context={
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(request,'test_form.html',context)

@login_required
@permission_required('tasks.change_task', login_url='no_permission')
def update_task(request, id):
    # employees=Employee.objects.all()
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) # For GET
    if task.taskDetails:
        task_detail_form = TaskDetailModelForm(instance=task.taskDetails) # GET operation

    if request.method == 'POST':
        # form = TaskForm(request.POST, employees=employees) # For Django Basic Form POST
        task_form = TaskModelForm(request.POST, instance=task) # For Django Model Form
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.taskDetails)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ For Django Model Form """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request,'Task Updated Successfully')
            return redirect('update_task',id)
            # return render(request, 'test_form.html', {"task_form":task_form,"task_detail_form":task_detail_form,"message":"Data is successfully added"})
            """ For Django Basic Form  Data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task=Task.objects.create(title=title, description=description, due_date=due_date)

            # # Assign employee to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            
            # return HttpResponse('Task Added Successfully')

    context={
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(request,'test_form.html',context)

@login_required
@permission_required('tasks.delete_task', login_url='no_permission')
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task is deleted successfully")
        
        return redirect('manager_dashboard')

@login_required
@permission_required('tasks.view_task', login_url='no_permission')
def view_task(request):
    # Retrieve all data of Task model
    # tasks=Task.objects.all()

    # Retrieve specific data get by id
    # task_3=Task.objects.get(id=1)

    # Retrieve specific data get by first
    # task_4=Task.objects.first()

    # Retrieve task details by primary key (pk)
    # task_5 = Task.objects.get(pk=1)
    
    # return render (request,'show_task.html',{'tasks':tasks, 'task_3':task_3, 'task_4':task_4, 'task_5': task_5})

    # Get specific data by filtering
    # tasks=Task.objects.filter(status='PENDING')

    # show the task by
    # tasks = Task.objects.filter(due_date=date.today())

    """ Show the task which priority is not low"""
    # tasks=TaskDetail.objects.exclude(priority="L")

    """ Show the task which priority is not high"""
    # tasks=TaskDetail.objects.exclude(priority="H")

    """Show the task that contain word 'paper' and status PENDING """
    # tasks=Task.objects.filter(title__icontains = "p", status="PENDING")
    
    """Show the task that contains which are pending or in-progress"""
    # tasks=Task.objects.filter(Q(status="PENDING")|Q(status="IN_PROGRESS"))
    
    # tasks=Task.objects.filter(status="aldfjasldfk").exists()


    """ select__related (ForeignKey, OneToOneField)"""
    # tasks = Task.objects.all()
    # tasks = Task.objects.select_related('details').all()
    # tasks = TaskDetail.objects.select_related('task').all()
    # tasks = Task.objects.select_related('project').all()

    """ Prefetch__related. It's works for (Foreign Key, ManyToMany)"""
    # tasks = Project.objects.prefetch_related('projects').all()
    # return render(request,'show_task.html',{'tasks':tasks})

    """Aggregate Function"""
    # task_count = Task.objects.aggregate(num_task=Count('id'))
    # return render(request,'show_task.html',{'task_count':task_count})

    projects=Project.objects.annotate(num_task=Count('tasks')).order_by('num_task')
    return render(request,'show_task.html',{'projects':projects})

@login_required
@permission_required('tasks.view_task', login_url='no_permission')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES
    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task_details', task.id)
    return render(request, 'task_details.html',{'task':task, 'status_choices':status_choices})


# @login_required
# @permission_required('tasks.view_task',login_url='no_permission')
# def change_task(request):
@login_required
def dashboard(request):
    if is_Manager(request.user):
        return redirect('manager_dashboard')
    elif is_Employee(request.user):
        return redirect('user_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')
    
    return redirect('no_permission')