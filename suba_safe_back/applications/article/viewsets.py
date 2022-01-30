# Third-Party Apps Imports
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

# Imports de Django 
from django.shortcuts import get_object_or_404

# Imports de los modelos
from applications.category.models import Category
from .models import Article

# Imports de los serializadores
from .serializers import (
    ArticleProcessSerializer,
    ArticleSerializer,
)
             

class ArticleViewSet(viewsets.ModelViewSet):
    # Únicamente los usuarios con un token de acceso podrán 
    # usar a las operaciones CRUD
    authentication_classes = (
        TokenAuthentication,
        JWTAuthentication,
    )
    queryset = Article.article_objects.all()
    serializer_class = ArticleSerializer

    # Permisos para las aplicaciones
    def get_permissions(self):
        # Si el método es LIST o RETRIEVE
        if(self.action =='list' or self.action =='retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    # Override de LIST para obtener todas las ofertas
    def list(self, request):
        queryset = Article.article_objects.all()
        serializer = ArticleSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Override de CREATE para crear un artículo
    def create(self, request):
        serializer = ArticleProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category_id = serializer.validated_data['category']
        
        try:
            category = Category.objects.get(id=category_id)
            
            article = Article.article_objects.create(
                name = serializer.validated_data['name'],
                description = serializer.validated_data['description'],
                main_image = serializer.validated_data['main_image'],
                main_image_opt_text = serializer.validated_data ['main_image_opt_text'],
                image_1 = serializer.validated_data['image_1'],
                image_1_opt_text = serializer.validated_data['image_1_opt_text'],
                image_2 = serializer.validated_data['image_2'],
                image_2_opt_text = serializer.validated_data['image_2_opt_text'],
                image_3 = serializer.validated_data['image_3'],
                image_3_opt_text = serializer.validated_data['image_3_opt_text'],
                image_4 = serializer.validated_data['image_4'],
                image_4_opt_text = serializer.validated_data['image_4_opt_text'],
                starting_bid = serializer.validated_data['starting_bid'],
                category = category,
                seller = self.request.user,
            )
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        except Category.DoesNotExist:
            content = {'error': 'La Categoría no existe'}
            
            return Response(content, status = status.HTTP_404_NOT_FOUND)

    # Override de UPDATE para actualizar un artículo
    def update(self, request, pk=None):
        article = get_object_or_404(Article.article_objects.all(), pk=pk)
        
        serializer = ArticleProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category_id = serializer.validated_data['category']
        
        try:
            category = Category.objects.get(id=category_id)
            
            article = Article.article_objects.update(
                name = serializer.validated_data['name'],
                description = serializer.validated_data['description'],
                main_image = serializer.validated_data['main_image'],
                main_image_opt_text = serializer.validated_data ['main_image_opt_text'],
                image_1 = serializer.validated_data['image_1'],
                image_1_opt_text = serializer.validated_data['image_1_opt_text'],
                image_2 = serializer.validated_data['image_2'],
                image_2_opt_text = serializer.validated_data['image_2_opt_text'],
                image_3 = serializer.validated_data['image_3'],
                image_3_opt_text = serializer.validated_data['image_3_opt_text'],
                image_4 = serializer.validated_data['image_4'],
                image_4_opt_text = serializer.validated_data['image_4_opt_text'],
                starting_bid = serializer.validated_data['starting_bid'],
                category = category,
                seller = self.request.user,
            )
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        except Category.DoesNotExist:
            content = {'error': 'La Categoría no existe'}
            
            return Response(content, status = status.HTTP_404_NOT_FOUND)
        