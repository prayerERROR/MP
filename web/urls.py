from django.conf.urls import url
from web.views import account_views, home_views

urlpatterns = [
    url('^register/$', account_views.register, name='register'),
    url('^register/email-verify/$', account_views.email_verify, name='emailVerify'),
    url('^login/email/$', account_views.login_email, name='loginEmail'),
    url('^login/username/$', account_views.login_username, name='loginUsername'),
    url('^login/image-verify/$', account_views.image_verify, name='imageVerify'),
    url('^logout/$', account_views.logout, name='logout'),
    url('^index/$', home_views.index, name='index'),
]
