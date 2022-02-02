# Imports de Third-Party Apps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny,
)
from rest_framework import (
    viewsets,
    status,
)

# Imports de Django 
from django.shortcuts import get_object_or_404

# Imports de Serializadores 
from .serializers import (
    BidProcessSerializer,
    BidSerializer,
)

# Imports de Modelos 
from applications.article.models import Article
from applications.auction.models import Auction
from .models import Bid


# Validar si una oferta es mayor a la oferta inicial o actual
def is_valid(article, offer):
    if offer >= article.starting_bid and (article.current_bid is None or offer > article.current_bid):
        return True
    else:
        return False
    
    
# ViewSet para CRUD de un Proceso de Oferta
class BidProcessViewSet(viewsets.ViewSet):
    # Únicamente los usuarios con un token de acceso podrán  usar a las operaciones CRUD
    authentication_classes = (
        TokenAuthentication, 
        JWTAuthentication,
    )
    
    # Permisos para las aplicaciones
    def get_permissions(self):
        # Permisos de la vista
        if(self.action == 'list' or self.action == 'retrieve'):
            permission_classes = [AllowAny]
        elif (self.action == 'create'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
    
        return [permission() for permission in permission_classes]

    # Override de LIST para obtener todas las ofertas
    def list(self, request):

        queryset = Bid.objects.all()
        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)

    # Override de CREATE para hacer una oferta
    def create(self, request):
        serializer = BidProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article_id = serializer.validated_data['article']
        
        offer = serializer.validated_data.get('offer')
        
        # Recuperar un objeto Artículo del modelo Artículo
        try:
            try:
                article = Article.article_objects.get(id=article_id)
                auction = article.articulo_subasta.article

                # Comprobar si oferta es válida
                if is_valid(article, offer):
                    
                    #Crear objeto de tipo Subasta
                    bid = Bid.objects.create(
                        bidder = self.request.user,
                        offer = serializer.validated_data.pop('offer'),
                        article = article,
                    )

                    # Actualizar el valor de oferta actual del artículo
                    article.current_bid = offer
                    article.save()

                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    content = {'errors': 'La oferta no es válida'}
                    return Response(content, status = status.HTTP_400_BAD_REQUEST)

            except Article.DoesNotExist:
                content = {'errors': 'El artículo no existe'}
                return Response(content, status = status.HTTP_404_NOT_FOUND)
        
        # Sino encuentra objeto Artículo en Auction
        except Auction.DoesNotExist:
            content = {'errors': 'El artículo no tiene una subasta activa'}
            return Response(content, status = status.HTTP_404_NOT_FOUND)
    
    # Override de RETRIEVE para obtener una subasta específica
    def retrieve(self, request, pk=None):
        
        # Extraer objeto si lo halla o mostrar 404 si no. 
        bid = get_object_or_404(Bid.objects.all(), pk=pk)
        serializer = BidSerializer(bid)
        #
        return Response(serializer.data)
