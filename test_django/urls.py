"""test_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views import index, device_mgmt, device_monitor, login_system, file_mgmt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.index),
    path('add_device', device_mgmt.add_device),
    path('show_device', device_mgmt.show_device),
    path('edit_device/<int:id>', device_mgmt.edit_device),
    path('delete_device/<int:id>', device_mgmt.delete_device),
    path('device_monitor', device_monitor.device_monitor),
    path('device_monitor/<str:chart_type>/<int:deviceid>/', device_monitor.chart_json),
    path('file_mgmt', file_mgmt.upload),
    path('download/<int:id>', file_mgmt.download),
    path('accounts/login/', login_system.loginweb),
    path('accounts/logout/', login_system.logoutweb),
]
