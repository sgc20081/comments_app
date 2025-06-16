from django.urls import path

from .views import CustomTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='refresh_token')
]