from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/crop/', views.crop, name='crop'),
    path('dashboard/task/', views.task, name='task'),
    path('dashboard/inventory', views.inventory, name='inventory'),
    path('dashboard/worker/', views.worker, name='worker'),
    path('dashboard/equipment/', views.equipment, name='equipment'),
    path('dashboard/supplier/', views.supplier, name='supplier'),
]