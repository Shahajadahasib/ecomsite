from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=20)

    @staticmethod
    def get_all_categorys():
        return Category.objects.all()

    def __str__(self):
        return self.title
