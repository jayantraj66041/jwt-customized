import imp
from django.urls import path
from .views import UserSignupView, UserLoginView, UserRefreshTokenView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("signup/", UserSignupView.as_view()),

    path('login/', UserLoginView.as_view()),
    path('refresh/', UserRefreshTokenView.as_view()),
]