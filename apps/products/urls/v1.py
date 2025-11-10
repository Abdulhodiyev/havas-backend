
from django.urls import path

from apps.products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListAPIView.as_view(), name='list'),
    path('<int:pk>/', views.ProductRetrieveAPIView.as_view(), name='retrieve')
]
