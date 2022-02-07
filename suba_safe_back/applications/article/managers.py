from django.db import models


class ArticleManager(models.Manager):

    # Obtener productos por usuarios
    def articles_by_user(self, user):
        return self.filter(
            seller = user,
        )
    
    # Obtener productos por categoría
    def articles_by_category(self, category):
        return self.filter(
            category = category,
        ).order_by('category')
        
    # Obtener artículos activos
    def active_articles(self, is_active):
        return self.filter(
            is_active = is_active
        ).order_by('name')
        
    # Obtener artículos inactivos
    def inactive_articles(self, is_active):
        return self.filter(
            is_active = is_active
        ).order_by('name')
        
    # Obtener artículos activos por usuario
    def active_articles_by_user(self, is_active, user):
        return self.filter(
            is_active = is_active,
            seller = user
        ).order_by('name')
    
    # Obtener artículos inactivos por usuario
    def inactive_articles_by_user(self, user):
        return self.filter(
            buyer = user
        ).order_by('name')
        