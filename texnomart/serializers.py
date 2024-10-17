from rest_framework import serializers
from .models import Category, Product, Image, Order, Comment, AttributeKey, AttributeValue, ProductAttribute

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'slug']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_primary', 'product']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'message', 'file', 'product', 'user', 'rating']

class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = ['id', 'key_name']

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value_name']

class ProductAttributeSerializer(serializers.ModelSerializer):
    attr_key = AttributeKeySerializer(read_only=True)
    attr_value = AttributeValueSerializer(read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['id', 'attr_key', 'attr_value', 'product']


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'quantity', 'users_like', 'slug',
            'category', 'images', 'attributes', 'comment_count', 'is_liked'
        ]

    def get_comment_count(self, obj):
        return Comment.objects.filter(product=obj).count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.users_like.filter(id=user.id).exists()
        return False

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'first_payment', 'month', 'monthly_payment']