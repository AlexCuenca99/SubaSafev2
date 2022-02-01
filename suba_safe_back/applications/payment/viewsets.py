# Imports de Third-Party Apps 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets


# Imports de Django
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse

from applications.users.utils import Util

# Imports de Modelos
from applications.auction.models import Auction
from applications.article.models import Article
from .models import Payment

# Imports de Serializadores 
from .serializers import (
    PaymentProcessSerializer,
    PaymentSerializer,
)


# APIView para el proceso de pagos
class PaymentProcessViewSet(viewsets.ViewSet):
    # Únicamente los usuarios con un token de acceso podrán 
    # usar a las operaciones CRUD
    authentication_classes = (
        TokenAuthentication,
        JWTAuthentication,
    )

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
        queryset = Payment.objects.all()
        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data)

    # Override de CREATE para crear un proceso de subasta
    def create(self, request):
        serializer = PaymentProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #
        auction_id = serializer.validated_data['auction']

        # Si ya existe un pago en una subasta activa
        if Auction.objects.get(pk = auction_id).payment is not None:
            return Response({'Status': 'Ya existe un pago sobre la subasta'})
        else:
            # Recuperar un objeto Artículo en Artículo
            try:
                auction = Auction.objects.get(id=auction_id)
                
                article = Article.article_objects.get(id = auction.article.id)

                payment = Payment.objects.create(
                    amount = auction.article.current_bid,
                    user = self.request.user,
                    description = serializer.validated_data.pop('description'),
                    payment_type = serializer.validated_data.pop('payment_type'),
                    status_payment = serializer.validated_data.pop('status_payment'),
                    date_payment = timezone.now(),
                )

                article.buyer = self.request.user
                article.is_active = False
                article.save()

                auction.payment = payment
                auction.save()

                # Envío de correo electrónico cuando se cierra una subasta. 
                current_site = get_current_site(request).domain
                relativeLink = reverse('payment_app:confirmar-pago')
                #absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                email_body = '¡En hora buena ' + str(self.request.user) + '!\n' + 'Haz ganado la subasta del artículo: ' + str(article.name) + '\n' + 'El precio que tienes que pagar es: ' + str(article.current_bid) + ' $'
                data = {
                    'email_body': email_body, 
                    'email_recipient': self.request.user,
                    'email_subject': 'Confirmación del Pago'
                }
                
                Util.send_email(data)
                return Response({'Status': 'Su pago se ha guardado.', 'Estado': 'Hay un ganador. Esperando la confirmación.'})
            except Auction.DoesNotExist:
                return Response({'Status': 'El artículo no tiene una subasta activa o no existe'})

    def retrieve(self, request, pk=None):
        # Extraer objeto si lo halla o mostrar 404 si no. 
        payment = get_object_or_404(Payment.objects.all(), pk=pk)
        serializer = PaymentSerializer(payment)
        #
        return Response(serializer.data)
