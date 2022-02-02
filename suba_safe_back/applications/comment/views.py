# Imports de Third-Party Apps
from rest_framework import (
    generics,
)

# Imports de Modelos 
from .models import Comment

# Imports de Serializadores 
from .serializers import CommentSerializer


# ListApiView para filtrar los comentarios por artículo
class CommentByArticleListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        article = self.kwargs['articulo']
        
        return Comment.comment_objects.comments_by_article(article)

