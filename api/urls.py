from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView ,GetShippingDetailsView,GetWishListItemView,GetWishListView, GetCategoriesView,GetCategoryView , GetProductsView ,GetProductView , GetReviewsView , GetRoutes,SendEmailView , GetCartItemView,GetCartView,GetCheckoutDetailsView

urlpatterns = [
    path('',GetRoutes.as_view(),name='api_routes'),
    path('api/register/', RegisterView.as_view(), name='register'),
  #  path('api/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/categories/',GetCategoriesView.as_view(), name='categories'),
    path('api/categories/<str:pk>/',GetCategoryView.as_view(), name='categories'),
    path('api/products/',GetProductsView.as_view(), name='products'),
    path('api/wishlist/',GetWishListView.as_view(), name='cart'),
    path('api/wishlist/<str:pk>/',GetWishListItemView.as_view(), name='cart_item'),

    path('api/cart/',GetCartView.as_view(), name='cart'),
    path('api/cart/<str:pk>/',GetCartItemView.as_view(), name='cart_item'),
    path('api/checkout/',GetCheckoutDetailsView.as_view(), name='checkout'),
    path('api/shipping/',GetShippingDetailsView.as_view(), name='checkout'),

    path('api/send_email/',SendEmailView.as_view(), name='checkout'),

    path('api/products/<str:pk>/',GetProductView.as_view(), name='product'),
    path('api/products/<str:pk>/reviews/',GetReviewsView.as_view(), name='reviews'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
]