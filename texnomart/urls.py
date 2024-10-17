from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ImageViewSet, OrderViewSet, CommentViewSet,
    AttributeKeyViewSet, AttributeValueViewSet, ProductAttributeViewSet,
    CategoryProductsView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'images', ImageViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'attribute-keys', AttributeKeyViewSet)
router.register(r'attribute-values', AttributeValueViewSet)
router.register(r'product-attributes', ProductAttributeViewSet)

urlpatterns = [
    path('', include(router.urls)),


    path('category/<slug:category_slug>/', CategoryProductsView.as_view(), name='category-products'),
]