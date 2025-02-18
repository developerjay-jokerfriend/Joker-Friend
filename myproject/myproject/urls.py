"""myproject URL Configuration

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
from django.urls import path, include
from . import views 
from django.conf import settings #custom import for storing images to media folder.
from django.conf.urls.static import static #custom import for storing images to media folder.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('capitalize/', views.capitalize, name='capitalize'),
    path('resultcaps/', views.resultcaps, name='resultcaps'),
    path('shop/',include('shop.urls')),
    path('blog/', include('blog.urls')),
    path('jokerfriend/', include('jokerfriend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #custom import for storing images to media folder.

