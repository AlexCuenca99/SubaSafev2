# Third-Party Apps
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
import stripe

from django.shortcuts import redirect
from django.conf import settings
from django.views import generic

from applications.article.models import Article

from .serializers import PaymentSerializer

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY


class ArticleLandingPageTemplateView(generic.TemplateView):
    template_name = 'payment.html'
    def get_context_data(self, **kwargs):
        article = Article.article_objects.get(name = '')
        context = super(ArticleLandingPageTemplateView, self).get_context_data(**kwargs)
        context.update({
            'article': article
        })
        return context


class StripeCheckoutSessionAPIView(views.APIView):
    def post(self, request):
        article_id = self.kwargs['articulo']
        article = Article.article_objects.get(id = article_id)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            'unit_amount': article.current_bid,
                            "product_data": {
                                "name": article.name,
                                'images': [article.main_image],
                            },
                        },
                        "quantity": 1,
                    },
                ],
                customer_email="test@gmail.com",
                mode="payment",
                success_url = settings.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url = settings.SITE_URL + '?canceled=true',

            )
            return redirect(checkout_session.url)
        except:
            content = {'errors': 'La creación del checkout de Stripe ha fallado'}
            return Response(content, status.HTTP_400_BAD_REQUEST)
