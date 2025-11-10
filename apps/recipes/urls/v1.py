
from django.urls import path

from apps.recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipesListAPI.as_view(), name='list'),
    path('<int:pk>/', views.RecipeDetailAPI.as_view(), name='detail'),
    path('recipes/create/', views.RecipeCreateAPIView.as_view()),
]
