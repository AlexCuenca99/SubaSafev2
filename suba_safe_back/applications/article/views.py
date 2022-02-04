# Imports de Third-Party Apps
from rest_framework import generics

# Imports de serializadores
from .serializers import ArticleSerializer

# Imports de modelos
from .models import Article


# Vista para filtrar los articulos por usuario
class ListAPIViewArticleByUser(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        return Article.article_objects.articles_by_user(user)


# Vista para filtrar los artículos por categoría
class ListApiViewArticleByCategory(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = self.kwargs['categoria']
        return Article.article_objects.articles_by_category(category)

# Vista para filtrar los artículos activos
class ActiveArticlesListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        is_active = True       
        return Article.article_objects.active_articles(is_active)
    
# Vista para filtrar los artículos no disponibles
class InactiveArticlesListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        is_active = False       
        return Article.article_objects.inactive_articles(is_active)
    

# Vista para filtrar los artículos disponibles por usuario
class ActiveArticlesByUserListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        is_active = True
        user = self.request.user
        
        return Article.article_objects.inactive_articles_by_user(is_active, user)


# Vista para filtrar los artículos inactivos por usuario
class InactiveArticlesByUserListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        is_active = False
        user = self.request.user
        
        return Article.article_objects.inactive_articles_by_user(is_active, user)
