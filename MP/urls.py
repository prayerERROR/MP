from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/register/', views.register),
    url(r'^app/email_verification', views.email_verification),
]
