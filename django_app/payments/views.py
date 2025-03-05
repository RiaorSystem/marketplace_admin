import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .mpesa import lipa_na_mpesa
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .mpesa import process_mpesa_payment

class MpesaPaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")

        if not phone_number or not amount:
            return Response({"error": "Phone number and amount are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = lipa_na_mpesa(phone_number, amount)
        return Response(response, status=status.HTTP_200_OK)
    
@csrf_exempt
def mpesa_webhook(request):
    if request.method == "GET":
        return JsonResponse({"message": "M-Pesa Webhook Active"}, status=200)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            response = process_mpesa_payment(data)
            return JsonResponse(response)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=400)