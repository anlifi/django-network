from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.profile, name="profile"),
    path("register", views.register, name="register"),
    
    path("htmx/post-form/", views.post_form, name="post_form"),
]

router = routers.DefaultRouter()
router.register("api/users", views.UserViewSet)
router.register("api/posts", views.PostViewSet)
router.register("api/likes", views.LikeViewSet)
router.register("api/followers", views.FollowerViewSet)

urlpatterns += router.urls
