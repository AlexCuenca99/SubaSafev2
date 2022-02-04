from django.urls import path, include

from . import views

app_name = 'article_app'

urlpatterns = [
    path('articulos/por-usuario/', views.ListAPIViewArticleByUser.as_view(), name='articulo-por_usuario/'),
    path('articulos/por-categoria/<categoria>/', views.ListApiViewArticleByCategory.as_view(), name='articulo-por_categoria'),
    path('articulos/activos/', views.ActiveArticlesListAPIView.as_view(), name='articulos-activos'),
    path('articulos/inactivos/', views.InactiveArticlesListAPIView.as_view(), name='articulos-inactivos'),
    path('articulos/activos/usuarios', views.ActiveArticlesByUserListAPIView.as_view(), name='articulos-activos_por_usuario'),
    path('articulos/inactivos/usuarios', views.InactiveArticlesByUserListAPIView.as_view(), name='articulos-inactivos_por_usuario'),
]