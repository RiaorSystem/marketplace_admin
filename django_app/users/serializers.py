from rest_framework import serializers
from .models import CustomUser, UserRoles, Contact
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.core.files.images import get_image_dimensions

class UserSerializer(serializers.ModelSerializer):
    class Meta:  
        
        model = CustomUser
        fields = ['first_name','last_name', 'email', 'phone_number']
        read_only_fields = ['id', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration (No profile picture upload here)"""
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=UserRoles.choices, default=UserRoles.BUYER)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password', 'role']

    def validate(self, data):
        """Ensure both passwords match."""
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from validated data
        password = validated_data.pop('password')

        # Generate username from email
        email = validated_data.get('email')
        validated_data['username'] = email.split('@')[0]  

        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash password
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
    

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing and updating user profile"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'bio', 'role']
        read_only_fields = ['email']

    def validate_profile_picture(self, value):
        if value:
            # Check file size (e.g., 2MB limit)
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Image size should not exceed 2MB.")
            
            # Check image dimensions (e.g., 500x500 max)
            width, height = get_image_dimensions(value)
            if width > 500 or height > 500:
                raise serializers.ValidationError("Image dimensions should not exceed 500x500 pixels.")
        return value

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=6)

    def validate(self, data):
        """Ensure old password is correct and new passwords match"""
        user = self.context['request'].user

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Incorrect old password."})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        return data
    
class ContactSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source="contact_user.username", read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "phone_number", "contact_user", "contact_name"]