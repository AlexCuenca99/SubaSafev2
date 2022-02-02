from django.urls import path, include

from . import views

app_name = 'article_app'

urlpatterns = [
    path('articulos/por-usuario/', views.ListAPIViewArticleByUser.as_view(), name='articulo-por_usuario/'),
    path('articulos/por-categoria/<categoria>/', views.ListApiViewArticleByCategory.as_view(), name='articulo-por_categoria'),
    path('articulos/activos/', views.ActiveArticles.as_view(), name='articulos-activos'),
    path('articulos/inactivos/', views.InactiveArticles.as_view(), name='articulos-inactivos')
]