from django.urls import path, include

from . import views

app_name = 'comment_app'

urlpatterns = [
    path('comentarios/por-articulo/<articulo>', views.CommentByArticleListAPIView.as_view(), name='comentario-por_articulo'),
]