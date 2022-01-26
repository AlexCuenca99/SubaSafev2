from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager

from applications.payment.managers import PaymentManager
from applications.bid.managers import BidManager
from applications.comment.managers import CommentManager

#FIXME
# Hacer las migraciones
# Corregir los serializadores para la creación de un registro de usuarios


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otros'),
    )

    CITY_CHOICES = (
        ('0', 'Riobamba'),
        ('1', 'Quito'),
        ('2', 'Guayaquil'),
        ('3', 'Ambato'),
        ('4', 'Cuenca'),

        # FIXME
        # Añadir más ciudades del Ecuador
    )

    username = models.CharField('Usuario', max_length=20)
    email = models.EmailField('Correo Electrónico', unique=True)
    first_name = models.CharField('Nombres', max_length=20, blank=True)
    last_name = models.CharField('Apellidos', max_length=20, blank=True)
    gender = models.CharField('Género', max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField('Teléfono', max_length=10)
    city = models.CharField('Ciudad', max_length=20, choices=CITY_CHOICES, blank=True)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    user_objects = UserManager()
    payment_objects = PaymentManager()
    bid_objects = BidManager()
    comment_objects = CommentManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'acces': str(refresh.access_token)
        }
