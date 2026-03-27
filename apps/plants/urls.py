from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.analyze_plant, name='analyze_plant'),
    path('<int:pk>/', views.plant_detail, name='plant_detail'),
    path('list/', views.plant_list, name='plant_list'),
    path('confirm/', views.plant_confirm, name='plant_confirm'),
]