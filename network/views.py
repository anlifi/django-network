from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PostForm
from .models import User, Post, Like, Follower


def index(request):
    # Check if user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Return index page with empty form and all posts
    form = PostForm()
    posts = Post.objects.all().order_by("update_date")
    return render(request, "network/index.html", {
        "post_form": form,
        "posts": posts
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
            # Return new post confirmation partial
            return render(request, "network/post_form_confirm.html")
    
    # Return post form partial (including validation errors)
    return render(request, "network/post_form.html", {
        "post_form": form,
    })


@login_required
def profile(request):
    return render(request, "network/profile.html")


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
