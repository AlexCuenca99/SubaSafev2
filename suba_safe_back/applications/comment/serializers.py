from rest_framework import serializers

from .models import Comment

from applications.users.models import User


class CommentSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'title',
            'content',
            'user',
            'article',
            'created',
            'modified',
        )
    
    def get_user(self, obj):
        query_set = User.comment_objects.users_per_comment(obj.id)
        serialized_user = UsersInCommentSerializer(query_set, many=True).data
        return serialized_user


# Serializador para crear un comentario
class CommentProcessSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=300)
    article = serializers.IntegerField()
    
    
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