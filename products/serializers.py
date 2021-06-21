from rest_framework import serializers
from .models import *
from users.models import *


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'type', 'in_stock', 'image']


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    items = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total', 'items']

    def get_total(self, obj):
        return obj.cart_total()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']
