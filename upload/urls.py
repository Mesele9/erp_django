from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('view/<int:file_id>/', views.view_file, name='view_file'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)