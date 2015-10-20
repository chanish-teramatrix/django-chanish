"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from article.views import HelloTemplate
admin.autodiscover()

from article.views import dbview, dbdata

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','article.views.practice_template'),
    url(r'^hello/$','article.views.hello'),
    url(r'^hello_template/$','article.views.hello_template'),
    url(r'^practice_template/$','article.views.practice_template'),
    url(r'^hello_class_view/$', HelloTemplate.as_view()),
    url(r'^articles/', include('article.urls')),

    #user authorisation urls

    url(r'^accounts/login/$', 'article.views.login'),
    url(r'^accounts/auth/$', 'article.views.auth_view'),
    url(r'^accounts/logout/$', 'article.views.logout'),
    url(r'^accounts/loggedin/$', 'article.views.loggedin'),
    url(r'^accounts/invalid/$', 'article.views.invalid_login'),
    url(r'^accounts/register/$', 'article.views.register_user'),
    url(r'^accounts/register_success/$', 'article.views.register_success'),
 

    url(r'^dbview/$', dbview.as_view()),
    url(r'^dbview/listing/$', dbdata.as_view(), name='db_view_listing'),


]
 