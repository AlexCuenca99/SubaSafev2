from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User

from django.contrib import auth


# Verficación del token generado por 
# medio de la autenticación de Google
class LoginSocialSerializer(serializers.Serializer):

    token_id = serializers.CharField(required=True)


# Serializador para los usuarios
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'password',
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
            'phone',
            'city',
        )


# Serializador para el registro de los usuarios
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, min_length=6, write_only=True)

    class Meta:
        model = User
        fields =[
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'gender',
            'phone',
            'city',
        ]
    
    def validate(self, data):
        email = data.get('email', '')
        username = data.get('username', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        gender = data.get('gender', '')
        phone = data.get('phone', '')
        city = data.get('city', '')

        if not first_name.isalpha():
            raise serializers.ValidationError('El nombre solo debe contener letras')
        
        if not last_name.replace(' ', '').isalpha():
            raise serializers.ValidationError('El apellidos solo debe contener letras')

        #if not(gender == 'M' or gender == 'F'):
        #    raise serializers.ValidationError('Ingrese un género válido')

        if not phone.isdecimal():
            raise serializers.ValidationError('El número de celular solo debe contener números')

        return data
    
    def create(self, validated_data):
        return User.user_objects.create_user(**validated_data)


# Serializador para validar una correo electrónico de un registro desde la app
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=25, min_length=2, write_only=True)
    username = serializers.CharField(max_length=25, min_length=2, read_only = True)
    tokens = serializers.CharField(max_length=25, min_length=2, read_only = True)
     
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'username',
            'tokens'
        ]

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        user = auth.authenticate(email = email, password = password)
        
        if not user:
            raise AuthenticationFailed('Credenciales no válidas. Intentalo de nuevo')
     
        if not user.is_active:
            raise AuthenticationFailed('La cuenta no está activa')

        return{
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        return super().validate(data)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
