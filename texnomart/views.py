from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product, Image, Order, Comment, AttributeKey, AttributeValue, ProductAttribute
from .serializers import (
    CategorySerializer, ProductSerializer, ImageSerializer,
    OrderSerializer, CommentSerializer, AttributeKeySerializer,
    AttributeValueSerializer, ProductAttributeSerializer
)
from rest_framework.permissions import IsAuthenticated


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AttributeKeyViewSet(viewsets.ModelViewSet):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer


class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer



class CategoryProductsView(APIView):
    serilaizer_class = CategorySerializer
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)


        products = Product.objects.filter(category=category)


        product_data = []
        for product in products:
            primary_image = Image.objects.filter(product=product, is_primary=True).first()
            serialized_product = ProductSerializer(product).data
            serialized_product['primary_image'] = primary_image.image.url if primary_image else None
            product_data.append(serialized_product)

        return Response(product_data)