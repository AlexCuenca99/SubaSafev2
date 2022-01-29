from rest_framework import serializers

from .models import Comment

from applications.users.models import User


class CommentSerializer(serializers.ModelSerializer):

    users = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'title',
            'content',
            'user',
            'users',
            'article',
            'created',
            'modified',
        )
    
    def get_users(self, obj):
        query_set = User.comment_objects.users_per_comment(obj.id)
        serialized_users = UsersInCommentSerializer(query_set, many=True).data
        return serialized_users


class UsersInCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'city',
        )