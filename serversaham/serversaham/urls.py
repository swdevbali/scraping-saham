"""serversaham URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from sahamapp.views import task_state, get_chart, index, linreg_view, linreg_process

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('saham/<perusahaan>/<durasi>', get_chart),
    path('celery/<task_id>', task_state, name='task_state'),
    path('linreg/form', linreg_view, name='linreg_view'),
    path('linreg/process', linreg_process, name='linreg_process'),

]
