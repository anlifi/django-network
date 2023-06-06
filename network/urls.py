from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("register", views.register, name="register"),
    
    path("htmx/all-posts", views.all_posts, name="all_posts"),
    path("htmx/post-form/", views.post_form, name="post_form"),
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
