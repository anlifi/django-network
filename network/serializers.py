from rest_framework import serializers
from .models import User, Post, Like, Follower


class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    username = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    likes = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'create_date', 'update_date', 'username', 'likes')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'date')


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('id', 'user', 'follows', 'date')