from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"User ID: {self.pk}, Username: {self.username}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} created post {self.pk} on {self.create_date}, last updated: {self.update_date}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.post.pk} liked by {self.user.username}"
    

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} started following {self.following}"
    
    def is_valid_follower(self):
        # User should not be able to follow himself
        return self.user != self.following
