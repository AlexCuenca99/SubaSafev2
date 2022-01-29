# Third-Party Apps Imports
from rest_framework import serializers

# Modelos Imports
from .models import Auction
from applications.article.models import Article


class AuctionSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = (
            'id',
            'start',
            'current_time',
            'article',
            'articles',
            'payment',
            'created',
            'modified',
        )
    
    def get_articles(self, obj):
        query_set = Article.auction_objects.articles_per_auction(obj.id)
        serialized_articles = ArticlesInAuctionSerializer(query_set, many=True).data
        #
        return serialized_articles


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


class AuctionProcessSerializer(serializers.Serializer):
    current_time = serializers.DateTimeField()
    article = serializers.IntegerField()
    payment = serializers.IntegerField(allow_null=True)
    