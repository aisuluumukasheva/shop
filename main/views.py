from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from .filters import ProductFilter


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    # permission_classes = [AllowAny,]
    # permission_classes = [IsAdminUser] # используется, если неи функции для запрета
    filterset_class = ProductFilter
    # filter_backends = [ProductFilter]
    # filterset_fields = ['category', 'status']

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'search']:
            # если это запрос на листинг или детализацию
            return [] #разрешаем всем
        return [IsAdminUser()]  # разрешаем только админам

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING)])
    @action(['GET'], detail=False)
    def search(self, request):
        # /products/search/?q=hello
        # query_params = {'q': 'hello'}
        q = request.query_params.get('q')
        queryset = self.get_queryset() # Product.object.all()
        if q:
            # queryset = queryset.filter(title__icontains=q)
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))  # поиск либо по названию либо по описанию (2 поиска)
        # queryset = Product.objects.filter(title__icontains=q) #icontains == ilike
        # get_serializer - ProductSerializer
        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
