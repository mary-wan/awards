from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import  UserRegisterForm,PostForm,RatingForm
from .models import Post,Rating
import random


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

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate_result.design_average = round(design_average, 2)
            rate_result.usability_average = round(usability_average, 2)
            rate_result.content_average = round(content_average, 2)
            rate_result.score = round(score, 2)
            rate_result.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingForm()
    params = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status,
        'current_user':current_user

    }
    return render(request, 'all-awards/project.html', params)

@login_required(login_url='login')
def user_profile(request, username):
    user_poster = get_object_or_404(User, username=username)
    if request.user == user_poster:
        return redirect('profile', username=request.user.username)
    user_posts = user_poster.posts.all()
    
    
    return render(request, 'all-awards/poster.html', {'user_poster': user_poster,'user_posts':user_posts})