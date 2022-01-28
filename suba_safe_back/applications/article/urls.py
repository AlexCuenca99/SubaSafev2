from django.urls import path, include

from . import views

app_name = 'article_app'

urlpatterns = [
    path('api/articulo/por-usuario', views.ListAPIViewArticleByUser.as_view(), name='articulo-por_usuario'),
    path('api/articulo/por-categoria/<category>', views.ListApiViewArticleByCategory.as_view(), name='articulo-por_categoria'),
]