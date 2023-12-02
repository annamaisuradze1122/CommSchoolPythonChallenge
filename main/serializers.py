from rest_framework import serializers
from . models import Product, RequestScrapper


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ScrapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestScrapper
        fields = '__all__'


