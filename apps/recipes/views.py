
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView

from apps.lists.models import Cart, CartProduct
from apps.products.models import Product
from apps.recipes.models import Recipe, RecipesProduct
from apps.recipes.serializers import RecipesListSerializer, RecipesDetailSerializer
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions.mobile import IsMobileUser
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.device import Device


class RecipesListAPI(ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = RecipesListSerializer
    permission_classes = [IsMobileUser | IsAuthenticated]

    def get_queryset(self):
        recipes = Recipe.objects.filter(is_active=True)
        category_id = self.request.GET.get('category_id')
        rating = self.request.GET.get('rating')
        min_calories = self.request.GET.get('min_calories')
        max_calories = self.request.GET.get('max_calories')
        min_cooking_time = self.request.GET.get('min_cooking_time')
        max_cooking_time = self.request.GET.get('max_cooking_time')
        order_by = self.request.GET.get('order_by')
        if category_id:
            recipes = recipes.filter(category_id=category_id)
        if rating:
            recipes = recipes.filter(avg_rating=int(rating))
        if min_calories:
            recipes = recipes.filter(calories__gte=int(min_calories))
        if max_calories:
            recipes = recipes.filter(calories__lte=int(max_calories))
        if min_cooking_time:
            recipes = recipes.filter(cooking_time__gte=int(min_cooking_time))
        if max_cooking_time:
            recipes = recipes.filter(cooking_time__lte=int(max_cooking_time))
        if order_by:
            recipes = recipes.order_by(order_by)
        return recipes


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)


class RecipeDetailAPI(RetrieveAPIView):
    serializer_class = RecipesDetailSerializer
    permission_classes = [IsMobileUser | IsAuthenticated]
    queryset = Recipe.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)


class RecipeCreateAPIView(CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipesDetailSerializer