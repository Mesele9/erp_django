
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path
from .views import (
    home, employee_list, employee_create, employee_update, employee_delete, employee_detail,
    department_list, department_create, department_update, department_delete, hr_dashboard,
    position_list, position_create, position_update, position_delete, 
    document_list, document_create, document_update, document_delete, document_upload_form,
    
)

app_name = 'hrms'

urlpatterns = [
    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    #path('', home, name='home'),
    path('', hr_dashboard, name='hr_dashboard'),
    
    # Employee Management
    path('employees/', employee_list, name='employee_list'),
    path('employees/create/', employee_create, name='employee_create'),
    path('employees/update/<int:pk>/', employee_update, name='employee_update'),
    path('employees/delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('employees/detail/<int:pk>/', employee_detail, name='employee_detail'),

    # Department Management
    path('departments/', department_list, name='department_list'),
    path('departments/create/', department_create, name='department_create'),
    path('departments/update/<int:pk>/', department_update, name='department_update'),
    path('departments/delete/<int:pk>/', department_delete, name='department_delete'),

    # Position Management
    path('positions/', position_list, name='position_list'),
    path('positions/create/', position_create, name='position_create'),
    path('positions/update/<int:pk>/', position_update, name='position_update'),
    path('positions/delete/<int:pk>/', position_delete, name='position_delete'),

    # Document Management
    path('documents/', document_list, name='document_list'),
    path('documents/create/', document_create, name='document_create'),
    path('documents/create/<int:employee_id>/', document_create, name='document_create_employee'),
    path('documents/update/<int:pk>/', document_update, name='document_update'),
    path('documents/delete/<int:pk>/', document_delete, name='document_delete'),
    path('documents/upload/', document_upload_form, name='document_upload_form'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
