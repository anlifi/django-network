from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("register", views.register, name="register"),
    
    path("htmx/posts/<str:type>", views.posts, name="posts"),
    path("htmx/posts/<str:type>/<str:username>", views.posts, name="posts"),
    path("htmx/post-form/", views.post_form, name="post_form"),
    path("htmx/post/<int:post_id>", views.post_view, name="post_view"),
    path("htmx/post/<int:post_id>/edit", views.post_edit, name="post_edit"),
    path("htmx/follow/<str:username>", views.follow, name="follow"),
    path("htmx/unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("htmx/profile-info/<str:username>", views.profile_info, name="profile_info"),
]

# router = routers.DefaultRouter()
# router.register("api/users", views.UserViewSet)
# router.register("api/posts", views.PostViewSet)
# router.register("api/likes", views.LikeViewSet)
# router.register("api/followers", views.FollowerViewSet)

# urlpatterns += router.urls
