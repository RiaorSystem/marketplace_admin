from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .mpesa import lipa_na_mpesa

class MpesaPaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")

        if not phone_number or not amount:
            return Response({"error": "Phone number and amount are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = lipa_na_mpesa(phone_number, amount)
        return Response(response, status=status.HTTP_200_OK)