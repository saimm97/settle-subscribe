"""
URL configuration for settlesubscribe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from os import name
from django.contrib import admin
from django.urls import path
from settle_subscribe import views
# from django.contrib.auth.urls import urls
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
# from user import views as user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('sign_in/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('sign_in/',views.login_page,name='login'),
    path('sign_up/',views.signup, name='signup'),   
    path('dashboard/',views.dashboard,name='dashboard'),

]
