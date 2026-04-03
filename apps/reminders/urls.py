from django.urls import path
from . import views
urlpatterns = [
    path('', views.list_reminders, name='list_reminders'),
    path('create/<int:plant_id>/', views.create_reminder, name='create_reminder'),
    path('complete/<int:reminder_id>/', views.complete_reminder, name='complete_reminder'),
    path('delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
]