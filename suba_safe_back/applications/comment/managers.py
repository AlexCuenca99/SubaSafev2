from django.db import models


class CommentManager(models.Manager):
    def users_per_comment(self, comment_id):
        query = self.filter(
            comment__id = comment_id
        )

        return query
    
    def comments_by_article(self, article_id):
        return self.filter(
            article_id = article_id
        ).order_by('article_id')