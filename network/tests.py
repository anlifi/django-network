from django.test import TestCase
from .models import User, Post, Like, Follower

# Create your tests here.
class PostTestCase(TestCase):

    def setUp(self):       
        # Create users
        u1 = User.objects.create(username="user1", email="user1@example.com")
        u2 = User.objects.create(username="user2", email="user2@example.com")

        # Create posts
        Post.objects.create(user=u1, content="aaa")
        Post.objects.create(user=u2, content="bbb")
        Post.objects.create(user=u1, content="ccc")

    def test_posts_count(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        with self.subTest():
            self.assertEqual(u1.posts.count(), 2)
        with self.subTest():
            self.assertEqual(u2.posts.count(), 1)
