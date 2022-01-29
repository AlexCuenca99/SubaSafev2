# Third-Party Apps Imports
from rest_framework import serializers

# Django Imports
from django.shortcuts import get_object_or_404

# Modelos Imports
from .models import Bid
from applications.article.models import Article
from applications.users.models import User


# Serializador que muestra todos los datos de una Oferta.
class BidSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    bidders = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = (
            'id',
            'article',
            'articles',
            'bidder',
            'bidders',
            'offer',
            'created',
            'modified',
        )
    
    def get_articles(self, obj):
        query_set = Article.bid_objects.articles_per_bid(obj.id)
        serialized_articles = ArticlesInAuctionSerializer(query_set, many=True).data
        return serialized_articles

    def get_bidders(self, obj):
        query_set = User.bid_objects.bidders_per_bid(obj.id)
        serialized_bidders = BiddersInAuctionSerializer(query_set, many=True).data
        return serialized_bidders


class ArticlesInAuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'id',
            'name',
            'description',
            'main_image',
            'image_1',
            'image_2',
            'image_3',
            'image_4',
            'is_active',
            'starting_bid',
            'current_bid',
            'category',
            'seller',
            'buyer',
            'watchers',
        )


class BiddersInAuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'city',
        )


class BidProcessSerializer(serializers.Serializer):
    offer = serializers.DecimalField(max_digits=7, decimal_places=2)
    article = serializers.IntegerField()


