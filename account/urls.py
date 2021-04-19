from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
    path('index/<workplace>', views.index, name='index'),
    path('sent/email', views.sent_mail, name='sent-email'),
    path('invite/users/<workplace>', views.invite_users, name='invite-users'),
    path('signup', views.signup, name='signup'),
    path('signup/<workplace>/<email>', views.signup_workplace, name='signup-workplace'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('activate/view/<email>', views.activate_email, name='activate-email'),
    path('activate/accounts/<email>', views.activate, name='activate'),
]