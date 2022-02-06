from django.urls import path

from . import viewsets

app_name = 'payment_app'

urlpatterns = [
    path('confirmar/pago/', viewsets.PaymentProcessViewSet, name='confirmar-pago'),
]