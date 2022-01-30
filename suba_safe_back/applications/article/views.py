# Imports de Third-Party Apps
from rest_framework.generics import ListAPIView

# Imports de serializadores
from .serializers import ArticleSerializer

# Imports de modelos
from .models import Article


# Vista para filtrar los articulos por usuario
class ListAPIViewArticleByUser(ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        return Article.article_objects.articles_by_user(user)


# Vista para filtrar los artículos por categoría
class ListApiViewArticleByCategory(ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = self.kwargs['categoria']
        return Article.article_objects.articles_by_category(category)