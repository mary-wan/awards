from django.urls import path
from django.conf.urls import url
from django.urls.conf import re_path

from projawards.serializers import PostSerializer
from . import views


urlpatterns = [
    path('',views.index, name='home'),
    path('project/<post>', views.project, name='project'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('profile/<username>/', views.profile, name='profile'),
    path('search/', views.search_project, name='search'),
    path('api/profile/', views.ProfileList.as_view()),
    path('api/post/', views.PostSerializer.as_view()),
    url(r'api/profile/profile-id/(?P<pk>[0-9]+)/$',views.ProfileDescription.as_view()),
    url(r'api/post/post-id/(?P<pk>[0-9]+)/$',views.PostDescription.as_view()),
    
]