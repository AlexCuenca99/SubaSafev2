# Imports de Third-Party Apps 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework import (
    viewsets,
    status,
)

# Django Imports
from django.shortcuts import get_object_or_404

# Imports de los modelos
from applications.article.models import Article
from .models import Comment

# Imports de los serializadores
from .serializers import (
    CommentSerializer,
    CommentProcessSerializer,
)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        TokenAuthentication, 
        JWTAuthentication
    )
    
    queryset = Article.article_objects.all()
    serializer_class = CommentSerializer

    # Permisos para las aplicaciones
    def get_permissions(self):
        # Si el método es LIST o RETRIEVE
        if(self.action =='list' or self.action =='retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    # Override de LIST para obtener todos los comentarios
    def list(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Override de CREATE para crear un comentario
    def create(self, request):
        serializer = CommentProcessSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        article_id = serializer.validated_data['article']
        
        # Recuperar objeto article_id en Artículo
        try:
            article = Article.article_objects.get(id=article_id)
            
            comment = Comment.objects.create(
                title = serializer.validated_data['title'],
                content = serializer.validated_data['content'],
                user = self.request.user,
                article = article
            )
                   
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            # return Response({'success': 'Comentario agregado'})
        
        except Article.DoesNotExist:
            content = {'error': 'Artículo no válido'}
            
            return Response(content, status = status.HTTP_404_NOT_FOUND)
    
    # Override de RETRIEVE para obtener un comentario específica
    def retrieve(self, request, pk=None):
        
        # Extraer objeto si lo halla o mostrar 404 si no. 
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        serializer = CommentSerializer(comment)
        #
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        # Extraer objeto si lo halla o mostrar 404 si no. 
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        serializer = CommentProcessSerializer(data = request.data)
                
        serializer.is_valid(raise_exception=True)
        article_id = serializer.validated_data['article']

        # Recuperar objeto article_id en Artículo
        try:
            article = Article.article_objects.get(id=article_id)
            
            comment = Comment.objects.update(
                title = serializer.validated_data['title'],
                content = serializer.validated_data['content'],
                user = self.request.user,
                article = article
            )
                   
            return Response(serializer.data, status = status.HTTP_200_OK)
            # return Response({'success': 'Comentario agregado'})
        
        except Article.DoesNotExist:
            content = {'error': 'Artículo no válido'}
            
            return Response(content, status = status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        # Extraer objeto si lo halla o mostrar 404 si no. 
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        serializer = CommentProcessSerializer(data = request.data)
        
        serializer.is_valid(raise_exception=True)
        article_id = serializer.validated_data['article']

        # Recuperar objeto article_id en Artículo
        try:
            article = Article.article_objects.get(id=article_id)
            
            comment = Comment.objects.update(
                title = serializer.validated_data['title'],
                content = serializer.validated_data['content'],
                user = self.request.user,
                article = article
            )
                   
            return Response(serializer.data, status = status.HTTP_200_OK)
            # return Response({'success': 'Comentario agregado'})
        
        except Article.DoesNotExist:
            content = {'error': 'Artículo no válido'}
            
            return Response(content, status = status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        # Extraer objeto si lo halla o mostrar 404 si no. 
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        comment.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)