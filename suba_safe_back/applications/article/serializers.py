# Imports de DRF
from rest_framework import serializers

# Imports de Modelos
from .models import Article

# Imports de Serializadores
from applications.users.serializers import UserPartialDataSerializer
from applications.category.serializers import CategorySerializer

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


# Serializador para crear un artículo
class ArticleProcessSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=400)
    main_image = serializers.ImageField()
    main_image_opt_text = serializers.CharField(max_length=50)
    image_1 = serializers.ImageField(required=False, default = 'no_image.png')
    image_1_opt_text = serializers.CharField(max_length=50, required=False, default = 'Texto alternativo')
    image_2 = serializers.ImageField(required=False, default = 'no_image.png')
    image_2_opt_text = serializers.CharField(max_length=50, required=False, default = 'Texto alternativo')
    image_3 = serializers.ImageField(required=False, default = 'no_image.png')
    image_3_opt_text = serializers.CharField(max_length=50, required=False, default = 'Texto alternativo')
    image_4 = serializers.ImageField(required=False, default = 'no_image.png')
    image_4_opt_text = serializers.CharField(max_length=50, required=False, default = 'Texto alternativo')
    starting_bid = serializers.DecimalField(max_digits=7, decimal_places=2)
    category = serializers.IntegerField()
    
    
# Serializador para mostrar todas la imágenes en un arreglo
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