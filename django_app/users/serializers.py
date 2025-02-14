from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile

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
        validated_data.pop('confirm_password')  # Remove confirm_password
        password = validated_data.pop('password')

        # Generate a unique username from email
        email = validated_data.get('email')
        validated_data['username'] = email.split('@')[0]  # Use email prefix as username

        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash password
        user.save()
        return user 
    
class SignInSerializer(serializers.Serializer): 
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio','profile_picture','date_of_birth','phone_number','address']