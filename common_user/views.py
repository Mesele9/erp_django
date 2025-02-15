
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
from .decorators import role_required, public_view

import qrcode
from io import BytesIO
import base64
from django.conf import settings


@public_view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            role_redirect = {
                'hr_staff': 'hr_dashboard',
                'store_staff': 'store_dashboard',
                'reception': 'upload_dashboard',
                'admin': 'admin_dashboard',
                'fb': 'menu_dashboard'
            }
            return redirect(role_redirect.get(user.role, 'login'))
            
        messages.error(request, 'Invalid credentials')
        return redirect('login')
        
    return render(request, 'common_user/login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@role_required('admin')
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    return render(request, 'common_user/admin_dashboard.html')


def is_admin(user):
    return user.is_superuser


@role_required('admin')
@login_required
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


@role_required('admin')
@login_required
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


def generate_qr_code(url, color='black'):
    """Helper function to generate QR code"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=color, back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

@public_view
def qr_code_page(request):
    # Generate URLs
    menu_url = request.build_absolute_uri('/menu')
    upload_url = request.build_absolute_uri('/upload')
    
    # Generate QR codes
    menu_qr = generate_qr_code(menu_url, color='#2c3e50')
    upload_qr = generate_qr_code(upload_url, color='#27ae60')
    
    context = {
        'menu_url': menu_url,
        'upload_url': upload_url,
        'menu_qr': menu_qr,
        'upload_qr': upload_qr,
    }
    return render(request, 'common_user/qr_code_page.html', context)
