# Third-Party Apps Imports
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import (
    viewsets, 
    status,
)

# Django Imports
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Serializadores Imports
from .serializers import (
    AuctionSerializer, 
    AuctionProcessSerializer
)

# Modelos Imports
from applications.article.models import Article
from .models import Auction


# Validar si un artículo sigue activo y si el tiempo de subasta es válido
def is_valid(article, current_time):
    if article.is_active and current_time > timezone.now():
        return 'both_valid'
    elif not article.is_active:
        return 'active_failure'
    else:
        return 'current_time_failure'


# ViewSet para CRUD de un Proceso de Subasta
class AuctionProcessViewSet(viewsets.ViewSet):
    # Únicamente los usuarios con un token de acceso podrán 
    # usar a las operaciones CRUD
    authentication_classes = (
        TokenAuthentication,
        JWTAuthentication,
    )
    
    # Permisos para las operaciones
    def get_permissions(self):
        # Si el método es LIST o RETRIEVE
        if(self.action =='list' or self.action =='retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        #
        return [permission() for permission in permission_classes]
    
    # Override de LIST para obtener todas las subastas
    def list(self, request):
        queryset = Auction.objects.all()
        serializer = AuctionSerializer(queryset, many=True)
        #
        return Response(serializer.data)

    # Override de CREATE para crear un proceso de subasta
    def create(self, request):
        serializer = AuctionProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #
        article_id = serializer.validated_data['article']
        current_time = serializer.validated_data.get('current_time')
        payment_id = serializer.validated_data['payment']

        # Recuperar un objeto Artículo en Subasta
        try:
            article = Auction.objects.get(article=article_id)
            #payment = Payment.objects.get(id=payment_id)
            
            # Si ya existe un artículo con una subasta activa
            if article:
                content = {'errors': 'Ya existe una subasta sobre el artículo'}
                return Response(content, status = status.HTTP_404_NOT_FOUND)

        # Si no encuentra objeto Artículo en Subasta
        except Auction.DoesNotExist:

            # Recuperar un objeto Artículo en Artículo
            try:
                article = Article.article_objects.get(id=article_id)

                # Comprobar si subasta es válida
                if is_valid(article, current_time) == 'both_valid':

                    #Crear objeto de tipo Subasta
                    auction = Auction.objects.create(
                        start = timezone.now(),
                        current_time = serializer.validated_data.pop('current_time'),
                        article = article,
                        payment = None
                    )
                    
                    content = {'messages': 'Subasta creada correctamente'}
                    return Response(content, status = status.HTTP_201_CREATED)   
                else:

                    # Comprobar cual es el tipo del error
                    if is_valid(article, current_time) == 'active_failure':
                        return Response({'Status': 'El artículo ya no está disponible'})
                    elif is_valid(article, current_time) == 'current_time_failure':
                        return Response({'Status': 'La fecha es errónea'})
            #
            # Sino encuentra objeto Artículo en Artículo
            except Article.DoesNotExist:
                content = {'errors': 'El artículo no existe'}
                return Response(content, status = status.HTTP_404_NOT_FOUND)

    # Override de RETRIEVE para obtener una subasta específica
    def retrieve(self, request, pk=None):

        # Extraer objeto si lo halla o mostrar 404 si no. 
        auction = get_object_or_404(Auction.objects.all(), pk=pk)
        serializer = AuctionSerializer(auction)
        #
        return Response(serializer.data)
