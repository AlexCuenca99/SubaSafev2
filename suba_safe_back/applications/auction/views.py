# Third-Party Apps Imports
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Modelos de la App Imports
from .models import Auction
from applications.article.models import Article

# Serializadores de la App Imports
from .serializers import AuctionSerializer


class AuctionAPIView(ListAPIView):
    pass
