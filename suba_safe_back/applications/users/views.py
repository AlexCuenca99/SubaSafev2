# Imports de Third Party Apps
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from drf_yasg import openapi
from rest_framework import (
    generics, 
    views,
)
import jwt

# Imports de Django
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import reverse

# Imports de Util
from .utils import Util

# Imports de Serializadores
from .serializers import (
    EmailVerificationSerializer,
    LoginSocialSerializer, 
    RegisterSerializer, 
    UserSerializer
)

# Imports de Modelos
from .models import User
    

class LoginUser(TemplateView):
    template_name = 'users/login.html'


# Registro de una cuenta usando Firebase (Google)
class GoogleLoginAPIView(views.APIView):

    serializer_class = LoginSocialSerializer

    def post(self, request):
        #Extraer lso datos enviados a traves de la petición
        serializer = self.serializer_class(data=request.data)

        # Validar serializador
        serializer.is_valid(raise_exception=True)

        # Extraer el token
        token = serializer.data.get('token_id')

        # Verificar si es un token FireBase válido
        decoded_token = auth.verify_id_token(token)

        username = decoded_token['name']
        email = decoded_token['email']
        email_verified = decoded_token['email_verified']

        user, created = User.user_objects.get_or_create(
            email = email,
            defaults={
                'username': username,
                'email': email,
                'is_active': email_verified,
            }
        )

        if created:
            token = Token.objects.create(user=user)
        else:
            token = Token.objects.get(user=user)

        user_get = {
            'id': user.pk,
            'email': user.email,
            'username': user.username,
            'gender': user.gender,
            'phone': user.phone,
            'city': user.city,
        }

        return Response(
            {
                'token': token.key,
                'user': user_get,
            }
        )


# API View para el registro de usuarios dentro de la app
class RegisterAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer =self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.user_objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('users_app:verificar-email')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = '¡Hola ' + user.username + '!\n' + 'Utiliza el siguiente enlace para verificar su correo electrónico\n' + absurl
        data = {
            'email_body': email_body, 
            'email_recipient': user.email,
            'email_subject': 'Verify your email'
        }
        
        Util.send_email(data)

        return Response(user_data, status = status.HTTP_201_CREATED)


# APIView para verificar por correo electrónico el registro de un usuario dentro de la app
class VerifyEmail(views.APIView):
    
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description = 'Description',
        type = openapi.TYPE_STRING
    )

    # Decorador para agregar un campo de forma manual en una petición GET              
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user = User.objects.get(id = payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'STATUS': 'El usuario ha sido activado'})
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'STATUS': 'El link de activación ha expirado'})
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'STATUS': 'El token de usuario ha expirado'})


# Vista para que un usuario autenticado pueda obtener sus datos
class UserAuthView(views.APIView):
    permission_class = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)