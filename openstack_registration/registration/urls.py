"""openstack_register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from registration import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_get_html),
    url(r'^policies', views.policies_get_html),
    url(r'^login', views.login),
    url(r'^register', views.register_dispatcher),
    url(r'^attributes$', views.attributes_dispatcher),
    url(r'^action/', views.activate_user),
    url(r'^users/(?P<username>[\w]+)$', views.user_dispatcher),
]