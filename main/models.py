from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,unique=True)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=255)
    image = models.URLField()
    rating_rate = models.FloatField()
    rating_count = models.IntegerField()

    def __str__(self):
        return f"Id: {self.product_id} ,  title : {self.title}"
        


