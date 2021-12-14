from django.http  import HttpResponseRedirect,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import  UpdateUserForm, UpdateUserProfileForm, UserRegisterForm,PostForm,RatingForm
from .models import Post, Profile,Rating
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer,ProfileSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets


def index(request):
    current_user = request.user
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = PostForm()
    
    try:
        posts = Post.objects.all()
        posts = posts[::-1]
        post_index = random.randint(0, len(posts)-1)
        random_post = posts[post_index]
        print(random_post.photo)
    except Post.DoesNotExist:
        posts = None
    return render(request, 'all-awards/home.html',{'form':form,'current_user':current_user,'random_post': random_post,'posts':posts})


def register(request):
    if request.user.is_authenticated:
    #redirect user to the profile page
        return redirect('home')
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
            
    else:
        form = UserRegisterForm()
    return render(request,"registration/register.html",{'form':form})

@login_required(login_url='login')
def project(request, post):
    post = Post.objects.get(title=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    current_user=request.user
    

    if request.method == "POST":
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        post_form = PostForm()
    
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate_result = form.save(commit=False)
            rate_result.user = request.user
            rate_result.post = post
            rate_result.save()
            post_ratings = Rating.objects.filter(post=post)

            design_rate = [d.design for d in post_ratings]
            design_av = sum(design_rate) / len(design_rate)

            usability_rate = [us.usability for us in post_ratings]
            usability_av = sum(usability_rate) / len(usability_rate)

            content_rate = [content.content for content in post_ratings]
            content_av = sum(content_rate) / len(content_rate)

            score = (design_av + usability_av + content_av) / 3
            print(score)
            rate_result.design_average = round(design_av, 2)
            rate_result.usability_average = round(usability_av, 2)
            rate_result.content_average = round(content_av, 2)
            rate_result.score = round(score, 2)
            rate_result.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingForm()
    return render(request, 'all-awards/project.html', {'post': post,'rating_form': form,'rating_status': rating_status,'current_user':current_user,'post_form':post_form})

@login_required(login_url='login')
def user_profile(request, username):
    current_user=request.user
    
    if request.method == "POST":
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        post_form = PostForm()
        
    user_poster = get_object_or_404(User, username=username)
    if request.user == user_poster:
        return redirect('profile', username=request.user.username)
    user_posts = user_poster.posts.all()
    
    
    return render(request, 'all-awards/poster.html', {'user_poster': user_poster,'user_posts':user_posts,'post_form':post_form,'current_user':current_user})

@login_required(login_url='login')
def profile(request, username):
    posts = request.user.posts.all()
    current_user=request.user
    
    if request.method == "POST":
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        post_form = PostForm()
        
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)

    return render(request, 'all-awards/profile.html', {'user_form':user_form,'profile_form':profile_form,'posts':posts,'post_form':post_form})

@login_required(login_url='login')
def search_project(request):
    if request.method == 'GET':
        title = request.GET.get("title")
        posts = Post.objects.filter(title__icontains=title).all()

    return render(request, 'all-awards/search.html', {'posts': posts})

   
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer