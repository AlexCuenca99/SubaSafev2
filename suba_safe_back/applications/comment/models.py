from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel

from applications.article.models import Article

class Comment(TimeStampedModel):
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Contenido', max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="articulo_comentarios")

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return str(self.id) + ' ' + str(self.article.name)

