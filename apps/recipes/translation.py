
from modeltranslation.translator import register, TranslationOptions
from .models import RecipesCategory, Recipe

@register(RecipesCategory)
class RecipesCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ('title',)
