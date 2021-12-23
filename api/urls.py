from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView , GetCategoriesView,GetCategoryView , GetProductsView ,GetProductView , GetReviewsView , GetRoutes

urlpatterns = [
    path('api/',GetRoutes.as_view(),name='api_routes'),
    path('api/register/', RegisterView.as_view(), name='register'),
  #  path('api/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/categories/',GetCategoriesView.as_view(), name='categories'),
    path('api/categories/<str:slug>/',GetCategoryView.as_view(), name='categories'),
    path('api/products/',GetProductsView.as_view(), name='products'),
    path('api/products/<str:pk>/',GetProductView.as_view(), name='product'),
    path('api/products/<str:pk>/reviews/',GetReviewsView.as_view(), name='reviews'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
]