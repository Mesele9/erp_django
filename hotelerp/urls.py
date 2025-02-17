from django.contrib import admin
from django.urls import path, include
from common_user.views import login_view, admin_dashboard, logout_view, qr_code_page, database_backup, database_restore
from employee_management.views import hr_dashboard
from upload.views import upload_dashboard
from store.views import store_dashboard
from comments.views import feedback_view, feedback_success_view, feedback_dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('admin/', admin.site.urls),
    path('hrms/', include("employee_management.urls")),
    path('store/', include("store.urls")),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    path('hr_dashboard/', hr_dashboard, name='hr_dashboard'),
    path('store_dashboard/', store_dashboard, name='store_dashboard'),
    path('upload_dashboard', upload_dashboard, name='upload_dashboard'),

    path('database_backup/', database_backup, name='database_backup'),
    path('database_restore/', database_restore, name='database_restore'),

    path('qr-codes/', qr_code_page, name='qr_code_page'),

    path('menu/', include('menu.urls')),

    path('upload/', include('upload.urls')),

    path('feedback/', feedback_view, name='feedback'),
    path('feedback-success/', feedback_success_view, name='feedback_success'),
    path('feedback-dashboard/', feedback_dashboard, name='feedback_dashboard'),

    path('room_directory/', include('directory.urls')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
