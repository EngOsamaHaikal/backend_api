from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/lgoin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
]