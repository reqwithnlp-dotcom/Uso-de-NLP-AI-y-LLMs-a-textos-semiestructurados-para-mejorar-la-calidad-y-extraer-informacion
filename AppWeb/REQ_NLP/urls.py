"""
URL configuration for REQ_NLP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
import os

def config_view(request):
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8001")
    return JsonResponse({"backend_url": backend_url})

urlpatterns = [
    path('admin/', admin.site.urls),
    path("config/", config_view),
    path('', include('req_nlp_app.urls')),  
    path('login/', auth_views.LoginView.as_view(template_name='req_nlp_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)