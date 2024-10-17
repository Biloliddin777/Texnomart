from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import (
    Category, Product, Image, Order, Comment,
    AttributeKey, AttributeValue, ProductAttribute
)
from .serializers import (
    CategorySerializer, ProductSerializer, ImageSerializer,
    OrderSerializer, CommentSerializer, AttributeKeySerializer,
    AttributeValueSerializer, ProductAttributeSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'slug']

    def get(self, request):
        cache_key = 'category_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            categories = self.filter_queryset(self.get_queryset())
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            cache.set(cache_key, serializer.data, timeout=60 * 3)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(cached_data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'slug']

    def get_queryset(self):
        cache_key = 'product_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            queryset = self.filter_queryset(Product.objects.all().select_related('category'))
            cache.set(cache_key, queryset, timeout=60 * 3)
            return queryset
        return cached_data


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
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'slug']

    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)

        products = self.filter_queryset(Product.objects.filter(category=category))

        product_data = []
        for product in products:
            primary_image = Image.objects.filter(product=product, is_primary=True).first()
            serialized_product = ProductSerializer(product).data
            serialized_product['primary_image'] = primary_image.image.url if primary_image else None
            product_data.append(serialized_product)

        return Response(product_data)
