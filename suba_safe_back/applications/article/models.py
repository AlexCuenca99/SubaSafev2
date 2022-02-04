from django.db import models
from django.conf import settings

from .managers import ArticleManager

from model_utils.models import TimeStampedModel

from applications.category.models import Category
from applications.auction.managers import AuctionManager
from applications.bid.managers import BidManager


# Modelo que representa a un artículo de la tienda
class Article(TimeStampedModel):
    name = models.CharField('Nombre', max_length=40)
    description = models.TextField('Descripción', max_length=400)
    main_image = models.ImageField('Imagen Principal', upload_to='articles/main')
    main_image_opt_text = models.CharField('Texto alt. Principal',max_length=50)
    image_1 = models.ImageField('Imagen 2', upload_to='articles/optional', blank=True, null=True, default = 'no_image.png')
    image_1_opt_text = models.CharField('Texto alt. 2', max_length=50, blank=True, null=True, default='Sin descripción')
    image_2 = models.ImageField('Imagen 3', upload_to='articles/optional', blank=True, null=True, default = 'no_image.png')
    image_2_opt_text = models.CharField('Texto alt. 3', max_length=50, blank=True, null=True, default='Sin descripción')
    image_3 = models.ImageField('Imagen 4', upload_to='articles/optional', blank=True, null=True, default = 'no_image.png')
    image_3_opt_text = models.CharField('Texto alt. 4', max_length=50, blank=True, null=True, default='Sin descripción')
    image_4 = models.ImageField('Imagen 5', upload_to='articles/optional', blank=True, null=True, default = 'no_image.png')
    image_4_opt_text = models.CharField('Texto alt. 5', max_length=50, blank=True, null=True, default='Sin descripción')
    is_active = models.BooleanField(default=True)
    starting_bid = models.DecimalField('Oferta Inicial', max_digits=7, decimal_places=2)
    current_bid = models.DecimalField('Oferta Actual', max_digits=7, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categoria_articulo')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuario_vendedor')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='usuario_comprador')
    watchers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='interesados_articulo')

    article_objects = ArticleManager()
    auction_objects = AuctionManager()
    bid_objects = BidManager()
    
    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.name)

