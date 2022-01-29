# Imports de DRF
from dataclasses import fields
from rest_framework import serializers

# Imports de Modelos
from .models import Article

# Imports de Serializadores
from applications.category.serializers import CategorySerializer
from applications.users.serializers import UserPartialDataSerializer

# Serializador para los artículos
class ArticleSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()

    category = CategorySerializer()
    seller = UserPartialDataSerializer()
    buyer = UserPartialDataSerializer()

    class Meta:
        model = Article
        fields = (
            'id',
            'name',
            'description',
            'images',
            'is_active',
            'starting_bid',
            'current_bid',
            'category',
            'seller',
            'buyer',
            'watchers',
            'created',
            'modified',
        )
    
    def get_images(self, obj):
        query_set = Article.article_objects.get(id = obj.id)
        serialized_objects = ImagesInArticleSerializer(query_set).data

        return serialized_objects


class ImagesInArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'main_image',
            'main_image_opt_text',
            'image_1',
            'image_1_opt_text',
            'image_2',
            'image_2_opt_text',
            'image_3',
            'image_3_opt_text',
            'image_4',
            'image_4_opt_text',
        )