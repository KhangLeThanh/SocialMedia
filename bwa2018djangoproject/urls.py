"""bwa2018djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from  funnysociety import views
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView


urlpatterns = [
    # url(r'^$', home, name='home'),
    url(r'^admin/', admin.site.urls), # Admin page
    url(r'^register/$', views.UserFormView.as_view(),name='register'), #User registration page
    url(r'^edit_profile/(?P<pk>[0-9]+)/$', views.edit_profile,name='edit_profile_with_pk'), #User edit page
    path('accounts/', include('django.contrib.auth.urls')), # User sign in, sign out default pages
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'), # Home page is the profile page
    path('', LoginView.as_view(template_name='registration/login.html'), name="home"),
  
    url(r'^profile/create_post/$', views.create_post,name='create_post'), #User registration page
    url(r'^profile/get_status/$', views.get_status,name='get_status'), #Get user status
    url(r'^profile/create_post/$', views.create_post,name='create_post'), #Add status post
    url(r'^profile/get_status/$', views.get_status,name='get_status'), #Get user status

    url(r'^profile/add_friend/$', views.add_friend,name='add_friend'), #Add friend
    url(r'^profile/get_friends/$', views.get_friends,name='get_friends'), #Get current friends
    

    #url(r'^profile/$', views.profile, name='profile'),


    # url(r'^discussion/$', views.discussion, name='discussion')
    #url(r'^event/$', event, name='event'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
