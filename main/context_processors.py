from users.models import Notification
import datetime


def main_context(request):
    today = datetime.date.today()
    is_superuser = False
    if "set_user_timezone" in request.session:
        user_session_ok = True
        user_time_zone = request.session['set_user_timezone']
    else:
        user_session_ok = False
        user_time_zone = "Asia/Kolkata"

    current_theme = 'cyan-600'
    current_role = "user"
    if request.user.is_authenticated():
        recent_notifications = Notification.objects.filter(user=request.user,is_deleted=False)
    else:
        recent_notifications = []

    active_parent = request.GET.get('active_parent')
    active = request.GET.get('active')
    
    return {
        'app_title' : "Default Application",
        "user_session_ok" : user_session_ok,
        "user_time_zone" : user_time_zone,
        "confirm_delete_message" : "Are you sure want to delete this item. All associated data may be removed.",
        "revoke_access_message" : "Are you sure to revoke this user's login access",
        "confirm_shop_delete_message" : "Your shop will deleted permanantly. All data will lost.",
        "confirm_delete_selected_message" : "Are you sure to delete all selected items.",
        "confirm_read_message" : "Are you sure want to mark as read this item.",
        "confirm_read_selected_message" : "Are you sure to mark as read all selected items.",
        'domain' : request.META['HTTP_HOST'],
        "current_theme" : current_theme,
        "is_superuser" : is_superuser,
        "active_parent" : active_parent,
        "active_menu" : active,
        "recent_notifications" : recent_notifications,
    }
