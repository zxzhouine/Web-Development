"""webapps URL Configuration

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
from django.urls import path,re_path,include
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
import grumblr.views
urlpatterns = [
path('index', grumblr.views.index,name='index'),
path('welcome',grumblr.views.home,name='welcome'),
path('login', auth_views.LoginView.as_view(template_name='grumblr/login.html'),name='login'),
path('register', grumblr.views.register,name='register'),
path('logout', grumblr.views.logout,name='logout'),
path('confirm/<str:username>/<str:token>', grumblr.views.confirm_email,name='confirm'),
path('reset_password_confirm/<str:username>/<str:token>', grumblr.views.reset_password_confirm,name='reset_password_confirm'),
path('set_password/<str:username>', grumblr.views.set_password,name='set_password'),
path('change-password/', grumblr.views.change_password,name='change_password'),
path('reset-password/', grumblr.views.reset_password,name='reset_password'),
path('create_post', grumblr.views.create_post,name='create_post'),
path('update_post', grumblr.views.update_post,name='update_post'),
path('create_comment/<str:post_id>/', grumblr.views.create_comment,name='create_comment'),
path('update_comment/', grumblr.views.update_comment,name='update_comment'),
re_path(r'^profile/(?P<user_username>[a-zA-Z0-9]+)$', grumblr.views.profile, name='profile'),
re_path(r'^photo/(?P<user_username>[a-zA-Z0-9]+)$', grumblr.views.get_photo,name='photo'),
re_path(r'^follow/(?P<user_username>[a-zA-Z0-9]+)$',grumblr.views.follow,name='follow'),
re_path(r'^unfollow/(?P<user_username>[a-zA-Z0-9]+)$',grumblr.views.unfollow,name='unfollow'),
path('followstream', grumblr.views.followstream,name='followstream'),
path('edit_profile', grumblr.views.edit_profile,name='edit_profile'),
path('error', grumblr.views.error,name='error'),
]