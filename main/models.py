from django.db import models


# Create your models here.
class Product(models.Model):
    car_id = models.IntegerField(primary_key=True)
    man_id = models.IntegerField()
    model_id = models.IntegerField()
    price_usd = models.FloatField()
    prod_year = models.IntegerField()
    price_value = models.IntegerField()

    def __str__(self):
        return self.name
    

class RequestScrapper(models.Model):
    link = models.CharField(max_length=255)
    status = models.CharField(max_length=256)
