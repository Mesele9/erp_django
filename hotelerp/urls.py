"""
URL configuration for hotelerp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from common_user.views import login_view, admin_dashboard, logout_view
from employee_management.views import hr_dashboard
from store.views import store_dashboard


urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('admin/', admin.site.urls),
    path('hrms/', include("employee_management.urls")),
    path('store/', include("store.urls")),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    path('hr_dashboard/', hr_dashboard, name='hr_dashboard'),
    path('store_dashboard/', store_dashboard, name='store_dashboard'),


]
