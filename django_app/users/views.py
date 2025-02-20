from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import SignInSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Signup Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  SignInView(APIView):
    def post(self,request):
        serializer = SignInSerializer(data = request.data)
        if serializer.is_valid():
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
