# Imports de Django
from django.conf import settings
from django.db import models

# Imports de Third-Party Apps
from model_utils.models import TimeStampedModel

# Imports de Modelos
from applications.article.models import Article


class Bid(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articulo_ofertas')
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuario_oferta')
    offer = models.DecimalField('Oferta', max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'

    def __str__(self):
        return 'Nº [' + str(self.id) + '] - ' + str(self.offer)
