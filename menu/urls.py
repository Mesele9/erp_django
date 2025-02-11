from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('item/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),

    path('qr-code/', views.generate_qr_code, name='generate_qr_code'),
    path('qr-code-page/', views.qr_code_page, name='qr_code_page'),
]