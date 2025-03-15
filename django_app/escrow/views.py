from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Advertisement, Escrow, AdvertisementApplication
from .serializers import AdvertisementSerializer, EscrowSerializer, AdvertisementApplicationSerializer
from .mpesa import lipa_na_mpesa
from rest_framework.generics import ListAPIView
from django.core.files.storage import default_storage

class CreateAdvertisementView(APIView):
    """Sellers create advertisement opportunities and place funds in escrow"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "seller":
            return Response({"error": "Only sellers can create advertisements"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AdvertisementSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            advertisement = serializer.save()

            # Create escrow record
            Escrow.objects.create(
                advertisement=advertisement,
                seller=request.user,
                amount=advertisement.budget
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApproveAdvertisementView(APIView):
    """Sellers approve advertisements and release escrow funds"""
    permission_classes = [IsAuthenticated]

    def post(self, request, ad_id):
        try:
            escrow = Escrow.objects.get(advertisement_id=ad_id, status="holding")
        except Escrow.DoesNotExist:
            return Response({"error": "Escrow not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if escrow.release_funds():
            return Response({"message": "Funds released to advertiser"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Escrow release failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class DepositToEscrowView(APIView):
    """Allows sellers to deposit funds into escrow"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "seller":
            return Response({"error": "Only sellers can deposit to escrow"}, status=status.HTTP_403_FORBIDDEN)
        
        payment_method = request.data.get("payment_method")
        amount = request.data.get("amount")
        phone_number = request.data.get("phone_number")

        if not amount or float(amount) <= 0:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        
        if payment_method == "mpesa": 
            response = lipa_na_mpesa(request.user, phone_number, float(amount))
            return Response(response, status=status.HTTP_200_OK)

        return Response({"error": "Unsupported payment method"}, status=status.HTTP_400_BAD_REQUEST)  

class SellerAdsView(ListAPIView):
    """View for sellers to see all their advertisements and applicants"""
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.filter(seller=self.request.user)
    
class AdApplicantsView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AdvertisementApplicationSerializer

    def get_queryset(self):
        ad_id = self.kwargs['ad_id']
        return AdvertisementApplication.objects.filter(advertisement__id=ad_id, advertisement__seller=self.request.user)
    
class ApplyForAdvertisementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ad_id):
        if request.user.role != "buyer":
            return Response({"error": "Only buyers can apply for adverisements"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            ad = Advertisement.objects.get(id=ad_id, is_active=True)
        except Advertisement.DoesNotExist:
            return Response ({"error": "Advertisement not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['advertiser'] = request.user.id
        data['advertisement'] = ad_id

        serializer = AdvertisementApplicationSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       

class SubmitAdvertisementStatsView(APIView):
    """Submission of engagement stats after running an ad"""
    permission_classes = [IsAuthenticated] 

    def post(self, request, application_id):
        try:
            application = AdvertisementApplication.objects.get(id=application_id, advertiser=request.user)
        except AdvertisementApplication.DoesNotExist:
            return Response ({"error": "Application not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        engagement_photo = request.FILES.get("engagement_photo")
        engagement_link = request.data.get("engagement_link")

        if not engagement_photo and not engagement_link:
            return Response({"error": "Either engagement photo or link is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if engagement_photo:
            file_path = default_storage.save(engagement_photo.name, engagement_photo)
            application.engagement_photo = file_path
        
        if engagement_link:
            application.engagement_link = engagement_link
        
        application.is_completed = True
        application.save()

        return Response({"message": "Engagement stats submited"}, status=status.HTTP_200_OK)
    
class ApproveAdvertisementApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):
        try:
            application = AdvertisementApplication.objects.get(id=application_id, advertisement__seller = request.user)
        except AdvertisementApplication.DoesNotExist:
            return Response({"error": "Application not found or you don't own the advertisement"}, status=status.HTTP_404_NOT_FOUND)
        
        if application.is_completed:
            application.approved = True
            application.save()

            return Response({"message": "Funds released to advertiser"}, status=status.HTTP_200_OK)
        
        return Response ({"error": "Advertisement is not completed yet"}, status=status.HTTP_400_BAD_REQUEST)
