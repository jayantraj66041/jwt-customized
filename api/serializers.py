from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attr):
        username = attr.get('username')
        password = attr.get("password")
        user = ''

        user_count = User.objects.filter(username=username).count()

        if user_count != 0:
            user = User.objects.get(username=username).username
        else:
            user_count = User.objects.filter(email=username).count()
            if user_count==0:
                raise serializers.ValidationError("Invalid Credentials!")
            else:
                user = User.objects.get(email=username).username
        username = user

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        
        data = {}
        refresh = self.get_token(username)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
        

class UserSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        fields = ['username', 'email', 'password', 'password2']
        model = User

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError("Both password must be same.")
        return data

    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
