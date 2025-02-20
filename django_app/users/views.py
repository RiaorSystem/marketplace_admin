from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
<<<<<<< HEAD
from .serializers import RegisterSerializer
from .serializers import ProfileSerializer
from .models import Profile
=======
from .serializers import SignInSerializer
>>>>>>> 7f4e1be64385842b16a060c36cdf985ab7325bf1
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
<<<<<<< HEAD
from .serializers import SignInSerializer
=======
from .serializers import SignInSerializer, UserProfileSerializer, RegisterSerializer, ChangePasswordSerializer
>>>>>>> 7f4e1be64385842b16a060c36cdf985ab7325bf1
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics


class SignUpView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Signup Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  SignInView(APIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
<<<<<<< HEAD
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]     

    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response (serializer.data)

    def put(self,request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile,data=request.data,partial=True)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        profile = Profile.objects.get(user=request.user)
        profile = delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
=======
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'phone_number': user.phone_number,
                    'profile_picture': user.profile_picture.url if user.profile_picture else None,
                    'bio': user.bio
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    """View for changing user password"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 7f4e1be64385842b16a060c36cdf985ab7325bf1
