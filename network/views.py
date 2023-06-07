from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import F, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets, permissions

from .forms import PostForm
from .models import User, Post, Like, Follower
from .serializers import UserSerializer, PostSerializer, LikeSerializer, FollowerSerializer

POSTS_PER_PAGE = 10


def index(request):
    # Check if user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Return index page with empty form and all posts (10 per page)
    form = PostForm()
    posts = _get_posts(request, "all")
    posts = _get_paginator(request, posts)

    return render(request, "network/index.html", {
        "post_form": form,
        "posts": posts,
        "type": "all",
    })


@login_required
def following(request):
    posts = _get_posts(request, "following")
    posts = _get_paginator(request, posts)
    return render(request, "network/following.html", {
        "posts": posts,
        "type": "following",
    })


@login_required
def follow(request, username):
    if request.method == "POST":
        try:
            # Create follower
            user_to_follow = User.objects.get(username=username)
            follower = Follower.objects.create(user=request.user, follows=user_to_follow)
            follower.save()
            message = None
        except User.DoesNotExist and Follower.DoesNotExist:
            message = "Cannot follow user: User does not exist."
            pass
        
        # Set custom response headers
        headers = {
            "HX-Trigger": "unFollow"
        }
        # Return unfollow partial button
        return HttpResponse(render(request, "network/unfollow.html", {
            "profile_user": user_to_follow,
        }), headers=headers)
    
    # Return follow partial button
    return render(request, "network/follow.html", {
        "profile_user": user_to_follow,
        "message": message,
    })


@login_required
def unfollow(request, username):
    if request.method == "POST":
        try:
            # Delete follower
            user_to_unfollow = User.objects.get(username=username)
            follower = Follower.objects.get(user=request.user, follows=user_to_unfollow)
            follower.delete()
            message = None
        except User.DoesNotExist and Follower.DoesNotExist:
            message = "Cannot unfollow user: User does not exist."
            pass
        
        # Set custom response headers
        headers = {
            "HX-Trigger": "unFollow"
        }
        # Return follow partial button
        return HttpResponse(render(request, "network/follow.html", {
            "profile_user": user_to_unfollow,
        }), headers=headers)
    
    # Return unfollow partial button
    return render(request, "network/unfollow.html", {
        "profile_user": user_to_unfollow,
        "message": message,
    })


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


def posts(request, type:str, **username:str):
    # Return all posts partial
    if type == "user" and username:
        if not isinstance(username, str):
            username = username["username"]
        posts = _get_posts(request, type, username=username)
    else:
        posts = _get_posts(request, type)
    posts = _get_paginator(request, posts)

    return render(request, "network/posts.html", {
        "posts": posts,
        "type": type,
        "profile_username": username
    })


def post_form(request):
    # Get form if POST else create new form
    form = PostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # Save form data
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # Set custom response headers
            headers = {
                "HX-Trigger": "loadPosts"
            }
            # Return new post confirmation partial
            return HttpResponse(render(request, "network/post_form_confirm.html"), headers=headers)
    
    # Return post form partial (including validation errors)
    return render(request, "network/post_form.html", {
        "post_form": form,
    })


@login_required
def profile(request, username):
    try:
        # Get user profile
        profile_user = User.objects.get(username=username)
        profile_username = profile_user.username
        is_follower = True if Follower.objects.filter(user=request.user, follows=profile_user) else False
        posts = _get_posts(request, "user", username=username)
        posts = _get_paginator(request, posts)
        message = None
    except User.DoesNotExist:
        profile_user, is_follower, posts, profile_username = None
        message = "Cannot load profile: User does not exist."

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "is_follower": is_follower,
        "message": message,
        "posts": posts,
        "type": "user",
        "profile_username": profile_username,
    })


@login_required
def profile_info(request, username):
    try:
        # Get user profile
        profile_user = User.objects.get(username=username)
        message = None
    except User.DoesNotExist:
        message = "Cannot load profile info: User does not exist."

    return render(request, "network/profile_info.html", {
        "profile_user": profile_user,
        "message": message,
    })


def _get_paginator(request, posts):
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return posts


def _get_posts(request, type:str, **username:str):
    if type == "all":
        posts = Post.objects.all().order_by("-create_date")
    elif type == "following":
        following = Follower.objects.filter(user=request.user)
        posts = Post.objects.filter(user__in=[follower.follows for follower in following]).order_by("-create_date")
    elif type == "user":
        try:
            profile_user = User.objects.get(username=username["username"])
        except KeyError:
            profile_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise User.DoesNotExist
        posts = Post.objects.filter(user=profile_user).order_by("-create_date")
    return posts


### API Views

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class PostViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows posts to be viewed or edited
#     """
#     queryset = Post.objects.all().order_by("-create_date")
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.annotate(
#             username=F("user__username"),
#             likes_count=Coalesce(Count("likes"), 0),
#         )


# class LikeViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows likes to be viewed or edited
#     """
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class FollowerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows followers to be viewed or edited
#     """
#     queryset = Follower.objects.all()
#     serializer_class = FollowerSerializer
#     permission_classes = [permissions.IsAuthenticated]