from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:  
        
        model = CustomUser
        fields = ['first_name','last_name', 'email', 'phone_number']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']

    def validate(self, data):
        """Ensure both passwords match."""
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        password = validated_data.pop('password')

       
        email = validated_data.get('email')
        validated_data['username'] = email.split('@')[0]  

        user = CustomUser(**validated_data)
        user.set_password(password)  
        user.save()
        return user 
    
class SignInSerializer(serializers.Serializer): 
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email = data['email']
        password = data['password']

        user =  authenticate(username = email, password = password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        data['user'] = user
        return data