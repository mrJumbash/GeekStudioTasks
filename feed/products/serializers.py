from rest_framework import serializers
from .models import *

class ProductValidateSerializer(serializers.Serializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    price = serializers.FloatField()
    category_id = serializers.IntegerField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance

