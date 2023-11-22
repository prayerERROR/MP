from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('admin/', admin.site.urls),
    url('app/', include('app.urls', namespace='app')),
    url('', include('web.urls')),
]
