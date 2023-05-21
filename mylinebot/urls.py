"""
URL configuration for mylinebot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from foodlinebot import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback', views.callback),
    # path('foodlinebot/', include('foodlinebot.urls')) #包含應用程式的網址
    path('https://7d3a-114-36-66-27.ngrok-free.app//callback', admin.site.urls) #包含應用程式的網址
    
]

'''
urlpatterns = [
    path('callback', views.callback)
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('foodlinebot/', include('foodlinebot.urls')) #包含應用程式的網址
]
'''

