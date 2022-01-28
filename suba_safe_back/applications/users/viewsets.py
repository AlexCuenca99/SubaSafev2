from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from django.contrib.auth.hashers import make_password

from .models import User

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.user_objects.all()

    def create(self, request, *args, **kwargs):
        try:
            email = User.user_objects.get(email=request.data['email'])

            if email:
                return Response({'Status': 'Ya existe una cuenta asociada al correo ingresado'})

        except User.DoesNotExist:
            request.data['password'] = make_password(request.data['password'])
            
            return super().create(request, *args, **kwargs)
    

    def partial_update(self, request, *args, **kwargs):
        password = request.data['password']

        if password:
            request.data['password'] = make_password(password)
        else:
            request.data['password'] = request.user.password
        
        return super().update(request, *args, **kwargs)