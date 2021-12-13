from django.urls import path
from django.conf.urls import url
from django.urls.conf import re_path
from . import views


urlpatterns = [
    path('',views.index, name='home'),
    path('project/<post>', views.project, name='project'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
]