from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.analyze_plant, name='analyze_plant'),
    path('<int:pk>/', views.plant_detail, name='plant_detail'),
    path('list/', views.plant_list, name='plant_list'),
    path('confirm/', views.plant_confirm, name='plant_confirm'),
    path('discard/', views.plant_discard, name='plant_discard'),
    path('<int:pk>/delete/', views.plant_delete, name='plant_delete'),  
]