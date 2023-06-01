from django.contrib import admin
from .models import User, Post, Like, Follower

# Register your models here.
admin.register(User)
admin.register(Post)
admin.register(Like)
admin.register(Follower)