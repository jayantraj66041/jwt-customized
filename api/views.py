from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer, UserLoginSerializer

# Create your views here.
class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserLoginView(TokenViewBase):
    serializer_class = UserLoginSerializer
        


class UserRefreshTokenView(APIView):
    def get(self, request):
        pass