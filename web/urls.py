from django.conf.urls import url
from web.views import account_views

urlpatterns = [
    url('register/', account_views.register, name='register'),
    url('register-verify-email/', account_views.register_verify_email, name='registerVerifyEmail'),
]