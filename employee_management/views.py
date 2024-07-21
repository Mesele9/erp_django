from django.contrib import messages
from django.contrib.auth.decorators  import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from datetime import datetime
from .models import Employee, Department, Position, Document
from .forms import EmployeeForm, DepartmentForm, PositionForm, DocumentForm
from .utils import is_upcoming_birthday, calculate_service_duration



@login_required
def hr_dashboard(request):
    # Total number of employees
    active_employees = Employee.objects.filter(is_active=True)
    total_employees = Employee.objects.filter(is_active=True).count()

    # Employees by department
    department_data = active_employees.values('department__name').annotate(employee_count=Count('id'))

    # Employees by gender
    male_count = active_employees.filter(gender='M').count()
    female_count = active_employees.filter(gender='F').count()

   # COC certified distribution
    coc_certified_count = active_employees.filter(is_coc_certified=True).count()
    coc_not_certified_count = active_employees.filter(is_coc_certified=False).count()

    # Educational level distribution
    education_data = Employee.objects.filter(is_active=True).values('education_level').annotate(count=Count('education_level'))

    # Assign colors for each education level
    colors = ['#3e95cd', '#8e5ea2', '#3cba9f', '#e8c3b9', '#c4decc']
    for i, data in enumerate(education_data):
        data['color'] = colors[i % len(colors)]

    # List employees birthday coming in the next 7 days
    upcoming_birthdays = [employee for employee in active_employees if is_upcoming_birthday(employee)]

    context = {
        'department_data': department_data,
        'total_employees': total_employees,
        'male_count': male_count,
        'female_count': female_count,
        'coc_certified_count': coc_certified_count,
        'coc_not_certified_count': coc_not_certified_count,
        'education_data': education_data,
        'upcoming_birthdays': upcoming_birthdays
    }

    return render(request, 'dashboard.html', context)


@login_required
def employee_list(request):
    all_employees = Employee.objects.all().order_by('id')
    active_employees = all_employees.filter(is_active=True)
    inactive_employees = all_employees.filter(is_active=False)
    departments = Department.objects.all()

    status_filter = request.GET.get('status', 'active')
    if status_filter == 'inactive':
        employees = inactive_employees
    elif status_filter == 'all':
        employees = all_employees
    else:
        employees = active_employees

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        employees = employees.filter(first_name__icontains=search_query)

    # Department filter
    selected_department = request.GET.get('department', None)
    if selected_department:
        employees = employees.filter(department_id=selected_department)

    # Educational level filter
    education_filter = request.GET.get('education')
    if education_filter:
        employees = employees.filter(education_level=education_filter)

    # Collect Employee period of service from the 
    for employee in employees:
        ethiopian_hire_date = employee.hire_date
        if ethiopian_hire_date:
            employee.period_of_service = calculate_service_duration(ethiopian_hire_date)
        else:
            employee.period_of_service = "N/A"

    # paginator
    paginator = Paginator(employees, 15)  # Show 15 employees per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'employees': page_obj,
        'departments': departments,
        'status_filter': status_filter,
        'search_query': search_query,
        'selected_department': selected_department,
        'education_filter': education_filter,
        'is_paginated': True,
    }

    return render(request, 'employee_list.html', context)


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee Added successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form, 'employee':employee})


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('employee_list')


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    documents = Document.objects.filter(employee=employee)
    next_employee = Employee.objects.filter(is_active=True, id__gt=pk).order_by('pk').first()  # Get the next employee
    previous_employee = Employee.objects.filter(is_active=True, id__lt=employee.id).order_by('-pk').first() # Get the previous employee
    context = {'employee': employee,'previous_employee': previous_employee, 'next_employee': next_employee, 'documents': documents}
    return render(request, 'employee_detail.html', context)    


@login_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    paginator = Paginator(departments, 10)  # Show 10 positions per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'department_list.html', {'page_obj': page_obj})


@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})


@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form})


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, 'Department deleted successfully.')
    return redirect('department_list')


@login_required
def position_list(request):
    positions = Position.objects.all().order_by('name')
    paginator = Paginator(positions, 10)  # Show 10 positions per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'position_list.html', {'page_obj': page_obj})


@login_required
def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Position created successfully.')
            return redirect('position_list')
    else:
        form = PositionForm()
    return render(request, 'position_form.html', {'form': form})


@login_required
def position_update(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, 'Position updated successfully.')
            return redirect('position_list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'position_form.html', {'form': form})


@login_required
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    position.delete()
    messages.success(request, 'Position deleted successfully.')
    return redirect('position_list')


@login_required
def document_list(request):
    documents = Document.objects.all().order_by('date_uploaded')
    employee = Employee.objects.first()  # Example: Get the first employee

    search_query = request.GET.get('search_query')
    if search_query:
        documents = documents.filter(name__icontains=search_query)

    paginator = Paginator(documents, 10)  # Show 10 documents per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'document_list.html', {'page_obj': page_obj, 'employee': employee})


@login_required
def document_create(request, employee_id=None):
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
        # Creating a document from the employee detail page
        return document_upload_form(request, include_employee_field=False, employee=employee)
    else:
        # Creating a document from the document list page (require employee selection)
        return document_upload_form(request, include_employee_field=True)


@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully.')
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_upload_form.html', {'form': form})


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    messages.success(request, 'Document deleted successfully.')
    return redirect('document_list')


@login_required
def document_upload_form(request, include_employee_field=True, employee=None):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, include_employee_field=include_employee_field)
        if form.is_valid():
            document = form.save(commit=False)
            if employee:
                document.employee = employee
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('document_list')
    else:
        form = DocumentForm(include_employee_field=include_employee_field)

    if employee:
        context = {
            'employee': employee,
            'form': form,
        }
    else:
        context = {
            'form': form,
        }
    return render(request, 'document_upload_form.html', context)
