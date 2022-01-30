# Third-Party Apps Imports
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Django Imports
from django.shortcuts import get_object_or_404

# Serializadores Imports
from .serializers import (
    BidProcessSerializer,
    BidSerializer,
)

# Modelos Imports
from .models import Bid
from applications.article.models import Article
from applications.auction.models import Auction


# Validar si una oferta es mayor a la oferta inicial o actual
def is_valid(article, offer):
    if offer >= article.starting_bid and (article.current_bid is None or offer > article.current_bid):
        return True
    else:
        return False


# ViewSet para CRUD de un Proceso de Oferta
class BidProcessViewSet(viewsets.ViewSet):
    # Únicamente los usuarios con un token de acceso podrán 
    # usar a las operaciones CRUD
    authentication_classes = (TokenAuthentication,)

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
        queryset = Bid.objects.all()
        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)

    # Override de CREATE para crear un proceso de subasta
    def create(self, request):
        serializer = BidProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article_id = serializer.validated_data['article']
        offer = serializer.validated_data.get('offer')
        
        # Recuperar un objeto Artículo en Artículo
        try:
            article = Article.article_objects.get(id=article_id)

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

                return Response({'Status': 'La oferta es válida'})
            else:
                return Response({'Status': 'Su oferta no es válida'})
        
        # Sino encuentra objeto Artículo en Artículo
        except Auction.DoesNotExist:
            return Response({'Status': 'El artículo no tiene una subasta activa o no existe.'})   
    
    # Override de RETRIEVE para obtener una subasta específica
    def retrieve(self, request, pk=None):
        
        # Extraer objeto si lo halla o mostrar 404 si no. 
        bid = get_object_or_404(Bid.objects.all(), pk=pk)
        serializer = BidSerializer(bid)
        #
        return Response(serializer.data)

