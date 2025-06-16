from django.urls import path

from .views import RegisterAPIView, CustomTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='refresh_token')
]