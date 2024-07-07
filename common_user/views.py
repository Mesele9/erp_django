
# common_user/views.py
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from .db_backup_restore import backup_database, restore_database
from .forms import DatabaseBackupForm
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



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


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    return render(request, 'common_user/admin_dashboard.html')


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def database_backup(request):
    if request.method == 'POST':
        form = DatabaseBackupForm(request.POST)
        if form.is_valid():
            backup_location = form.cleaned_data['backup_location']
            try:
                backup_path = backup_database(backup_location)
                with open(backup_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/sql')
                    response['Content-Disposition'] = f'attachment; filename={os.path.basename(backup_path)}'
                    messages.success(request, 'Database backup created successfully.')
                    return response
            except Exception as e:
                messages.error(request, f'Error during backup: {str(e)}')
    else:
        form = DatabaseBackupForm()

    return render(request, 'common_user/backup.html', {'form': form})

@user_passes_test(is_admin)
def database_restore(request):
    if request.method == 'POST':
        backup_file = request.FILES.get('backup_file')
        if backup_file:
            try:
                restore_database(backup_file)
                messages.success(request, 'Database restored successfully.')
                return redirect('admin_dashboard')
            except Exception as e:
                messages.error(request, f'Error during restore: {str(e)}')

    return render(request, 'common_user/restore.html')
