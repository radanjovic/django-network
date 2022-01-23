from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import *
from .forms import *


def index(request):
    """Displaying all the posts"""
    form = PostForm()
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    likes = False # For when users are not logged in..
    
    # Getting likes
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)

    # Creating new post
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "network/index.html", {"page_obj":page_obj, "form":form})

    else:
        return render(request, "network/index.html", {"page_obj":page_obj, "form":form, "likes":likes})



def users(request, username):
    """Displaying user profiles"""

    # Follow/unfollow - since it wasn't specified that this feature should be asyng
    # for simplicity it was done with just python/django.
    if request.method == "POST":
        user = request.user
        profile = User.objects.get(username=username)
        followers = profile.followers
        if "follow" in request.POST:
            follow = Follow.objects.create(user=user, following=profile)
            follow.save()
        elif "unfollow" in request.POST:
            unfollow = Follow.objects.get(user=user,following=profile)
            unfollow.delete()

        return HttpResponseRedirect(reverse('users', args=(username,)))
        

    # Getting users
    profile = User.objects.get(username=username)
    # Getting posts
    posts = Post.objects.filter(user=profile).all().order_by("-created")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Getting followers and followings
    following = Follow.objects.filter(user=profile).all()
    followers = User.objects.get(username=username).followers.all()
    # Getting numbers of followers and following
    num_following = len(following)
    num_followers = len(followers)

    already_following = False
    likes = False
    
    # Getting likes
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)

    # Checking if user already follows profile.
    if request.user.is_authenticated:
        user = request.user
        for i in followers:
            if user == i.user:
                already_following = True

    return render(request, "network/profile.html", {
        "page_obj":page_obj, 
        "profile":profile,
        "num_following":num_following,
        "num_followers":num_followers,
        "following":already_following,
        "likes":likes
        })


@login_required
def following(request):
    """Displaying only posts from people user follows"""
    # Getting followers
    following = Follow.objects.values_list('following',flat= True).filter(user=request.user.id)
    # Getting posts
    posts = Post.objects.filter(user_id__in=set(following)).order_by('-created')
    # Paginating
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    likes = False # For when users are not logged in..
    
    # Getting likes
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)

    return render(request, "network/following.html", {"page_obj":page_obj, "likes":likes})


@csrf_exempt # For simplicity
@login_required
def edit(request, id):
    """Editing posts async with JS"""
    # Only put request can edit
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # If request is not put, for safety redirect to index page
    else:
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt # For simplicity
@login_required
def like(request, id):
    # Only PUT can like/unlike
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        user = request.user

        data=json.loads(request.body)
        if data.get("action") == "like":
            like = Like.objects.create(user=user, post=post)
            like.save()
            post.like_count = data["like_count"]
            post.save()
        elif data.get("action") == "unlike":
            unlike = Like.objects.get(user=user, post=post)
            unlike.delete()
            post.like_count = data["like_count"]
            post.save()
        return HttpResponse(status=204)

    # If request is not put, for safety redirect to index page
    else:
        return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
