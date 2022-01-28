# Third-Party Apps Imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework import viewsets


from .models import Article

from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    # Únicamente los usuarios con un token de acceso podrán 
    # usar a las operaciones CRUD
    authentication_classes = (TokenAuthentication,)
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
        
        return Response(serializer.data)
