# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_dashboard, name='store_dashboard'),

    # Item URLs
    path('items/', views.item_list, name='item_list'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),

    # Suppliers Record URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/new/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    
    # Purchase Record URLs
    path('purchase-records/', views.purchase_record_list, name='purchase_record_list'),
    path('purchase-records/new/', views.purchase_record_create, name='purchase_record_create'),
    path('purchase-records/<int:pk>/', views.purchase_record_detail, name='purchase_record_detail'),
    path('purchase/<int:pk>/edit/', views.purchase_record_edit, name='purchase_record_edit'),
    path('purchase/<int:pk>/delete/', views.purchase_record_delete, name='purchase_record_delete'),

    
    # Issue Record URLs
    path('issue-records/', views.issue_record_list, name='issue_record_list'),
    path('issue-records/new/', views.issue_record_create, name='issue_record_create'),
    path('issue-records/<int:pk>/', views.issue_record_detail, name='issue_record_detail'),
    path('issue/<int:pk>/edit/', views.issue_record_edit, name='issue_record_edit'),
    path('issue/<int:pk>/delete/', views.issue_record_delete, name='issue_record_delete'),
    
    # Report URL
    path('generate-report/', views.generate_report, name='generate_report'),
    path('purchase-report/', views.purchase_report, name='purchase_report'),
    path('issue-report/', views.issue_report, name='issue_report'),
    path('purchase-items-report/', views.purchase_items_report, name='purchase_items_report'),
    path('issue-items-report/', views.issue_items_report, name='issue_items_report'),

    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),

    
]

