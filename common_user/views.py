
# common_user/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.urls import reverse
#from employee_management.views import hr_dashboard


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.role)
            if user.groups.filter(name='hr_staff'):
                return redirect('employee_management:hr_dashboard')
            elif user.groups.filter(name='store_staff').exists():
                return redirect('store:store_dashboard')
            elif user.is_superuser:
                return redirect('admin_dashboard')
        else:
            return render(request, 'common_user/login.html', {'error': 'Invalid username or password'})
            messages.error(request, 'Invalid username or password')
    return render(request, 'common_user/login.html')


""" def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(username)
        if user is not None:
            login(request, user)
            print(user.groups)
            if (user.groups == 'hr_staff'):
                return redirect('hr_dashboard')
            elif user.groups.filter(name='store_staff').exists():
                return redirect('store_dashboard')
            elif user.is_superuser:
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'common_user/login.html')
 """

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    return render(request, 'common_user/admin_dashboard.html')
