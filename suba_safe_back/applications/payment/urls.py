# Imports de Django
from django.urls import path

# Imports de views
from . import views

app_name = 'payment_app'

urlpatterns = [
    path('pagos/create-checkout-session/', views.StripeCheckoutSessionAPIView.as_view(), name='create-checkout-session'),
    path('pagos/crear-sesion-checkout/<articulo>', views.ArticleLandingPageTemplateView.as_view(), name='crear-sesion-checkout'),
]