"""tecnicas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    # urls vista administracion
    url(r'^admin/', admin.site.urls, ),
    # urls de la app mactor
    url(r'^mactor/', include('apps.mactor.urls', namespace="mactor")),
    # urls de la app entrevista
    url(r'^entrevista/', include('apps.entrevista.urls', namespace="entrevista")),
    # urls vista control de usuarios paquete Registration
    url(r'^accounts/', include('registration.backends.default.urls'))
]
