from django.db import models
from .category import Category

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField()
    jls_extract_var = Category
    category = models.ForeignKey(
        jls_extract_var, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=200, default='', null=True, blank=True)
    image = models.ImageField(upload_to="uploads/products/")

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return_Product.get_all_products()
