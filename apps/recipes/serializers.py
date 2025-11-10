
from rest_framework import serializers

from apps.products.models import Product
from apps.recipes.models import Recipe, RecipesCategory, RecipesProduct
from apps.shared.mixins.translation_mixins import (
    TranslatedFieldsReadMixin
)


class RecipeTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['title', 'images']
    media_fields = ['images']


class InlineCategorySerializer(TranslatedFieldsReadMixin, serializers.ModelSerializer):
    class Meta:
        model = RecipesCategory
        fields = ['title']

    translatable_fields = ['title']


class RecipesListSerializer(RecipeTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer):
    category_title = InlineCategorySerializer(source='category')

    class Meta:
        model = Recipe
        exclude = ['is_active', 'created_at', 'updated_at', 'category']


class InlineProductSerializer(TranslatedFieldsReadMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title']

    translatable_fields = ['title', 'images']
    media_fields = ['image']


class RecipesDetailSerializer(RecipeTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer):
    category_title = InlineCategorySerializer(source='category')

    class Meta:
        model = Recipe
        exclude = ['is_active', 'created_at', 'updated_at', 'category']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, created = RecipesCategory.objects.get_or_create(**category_data)
        recipe = Recipe.objects.create(category=category, **validated_data)
        return recipe
