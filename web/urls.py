from django.conf.urls import url
from web.views import account_views

urlpatterns = [
    url('^register/$', account_views.register, name='register'),
    url('^register/email-verify/$', account_views.email_verify, name='emailVerify'),
    url('^login/email/$', account_views.login_email, name='loginEmail'),
    url('^login/username/$', account_views.login_username, name='loginUsername'),
]
