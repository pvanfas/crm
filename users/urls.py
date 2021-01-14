from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('check-notification/', views.check_notification, name='check_notification'),
    path('notifications/', views.notifications, name='notifications'),
    path('notification/delete/<str:pk>/', views.delete_notification, name='delete_notification'),
    path('delete-selected-notifications/', views.delete_selected_notifications, name='delete_selected_notifications'),
    path('notification/read/<str:pk>/', views.read_notification, name='read_notification'),
    path('read-selected-notifications/', views.read_selected_notifications, name='read_selected_notifications'),

    path('set-user-timezone/', views.set_user_timezone, name='set_user_timezone'),


]
