from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('item/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),

]