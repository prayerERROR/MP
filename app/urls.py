from django.conf.urls import url
from app import views

urlpatterns = [
    url('register/', views.register),
    url('email_verification/', views.email_verification),
]
