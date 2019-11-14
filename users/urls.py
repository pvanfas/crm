from django.conf.urls import url,include
import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    
    url(r'^check-notification/$', views.check_notification, name='check_notification'),
    url(r'^notifications/$', views.notifications, name='notifications'),
    url(r'^notification/delete/(?P<pk>.*)/$', views.delete_notification, name='delete_notification'),
    url(r'^delete-selected-notifications/$', views.delete_selected_notifications, name='delete_selected_notifications'),
    url(r'^notification/read/(?P<pk>.*)/$', views.read_notification, name='read_notification'),
    url(r'^read-selected-notifications/$', views.read_selected_notifications, name='read_selected_notifications'),
    
    url(r'^set-user-timezone/$', views.set_user_timezone, name='set_user_timezone'),
    
    
]