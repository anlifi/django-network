from django.test import TestCase
from ..models import User, Post, Like, Follower

# Create your tests here.

class UserTestCase(TestCase):

    def test_user_string(self):
        u = User.objects.create(username="user")
        self.assertEqual(str(u), f"User ID: {u.pk}, Username: user")


class PostTestCase(TestCase):

    def setUp(self):       
        # Create users
        u1 = User.objects.create(username="user1")
        u2 = User.objects.create(username="user2")

        # Create posts
        Post.objects.create(user=u1, content="aaa")
        Post.objects.create(user=u2, content="bbb")
        Post.objects.create(user=u1, content="ccc")

    def test_user_posts_count(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        with self.subTest():
            self.assertEqual(u1.posts.count(), 2)
        with self.subTest():
            self.assertEqual(u2.posts.count(), 1)
    
    def test_post_string(self):
        u = User.objects.get(username="user1")
        p = Post.objects.get(user=u, content="aaa")
        self.assertEqual(str(p), f"user1 created post {p.pk} on {p.create_date}, last updated: {p.update_date}")


class LikeTestCase(TestCase):

    def setUp(self):
        # Create user and post
        u1 = User.objects.create(username="user1")
        u2 = User.objects.create(username="user2")

        p1 = Post.objects.create(user=u1, content="aaa")
        p2 = Post.objects.create(user=u2, content="bbb")

        # Create likes
        Like.objects.create(user=u1, post=p1)
        Like.objects.create(user=u2, post=p1)
        Like.objects.create(user=u1, post=p2)

    def test_user_liked_count(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        with self.subTest():
            self.assertEqual(u1.liked.count(), 2)
        with self.subTest():
            self.assertEqual(u2.liked.count(), 1)

    def test_post_likes_count(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        p1 = Post.objects.get(user=u1, content="aaa")
        p2 = Post.objects.get(user=u2, content="bbb")
        with self.subTest():
            self.assertEqual(p1.likes.count(), 2)
        with self.subTest():
            self.assertEqual(p2.likes.count(), 1)
    
    def test_like_string(self):
        u1 = User.objects.get(username="user1")
        p1 = Post.objects.get(user=u1, content="aaa")
        l = Like.objects.get(user=u1, post=p1)
        self.assertEqual(str(l), f"Post {p1.pk} liked by user1")


class FollowerTestCase(TestCase):

    def setUp(self):       
        # Create users
        u1 = User.objects.create(username="user1")
        u2 = User.objects.create(username="user2")
        u3 = User.objects.create(username="user3")

        # Create followers
        Follower.objects.create(user=u1, follows=u2)
        Follower.objects.create(user=u2, follows=u2)
        Follower.objects.create(user=u3, follows=u2)

    def test_following_count(self):
        u = User.objects.get(username="user1")
        self.assertEqual(u.following.count(), 1)
    
    def test_followers_count(self):
        u = User.objects.get(username="user2")
        self.assertEqual(u.followers.count(), 3)

    def test_follower_string(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        f = Follower.objects.get(user=u1, follows=u2)
        self.assertEqual(str(f), "user1 started following user2")
    
    def test_valid_follower(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        u3 = User.objects.get(username="user3")
        f1 = Follower.objects.get(user=u1, follows=u2)
        f2 = Follower.objects.get(user=u3, follows=u2)
        with self.subTest():
            self.assertTrue(f1.is_valid_follower())
        with self.subTest():
            self.assertTrue(f2.is_valid_follower())

    def test_invalid_follower(self):
        u = User.objects.get(username="user2")
        f = Follower.objects.get(user=u, follows=u)
        self.assertFalse(f.is_valid_follower())
