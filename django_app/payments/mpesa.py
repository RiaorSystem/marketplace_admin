import requests
import base64
from datetime import datetime
from django.conf import settings
from orders.models import Order

def get_mpesa_access_token():
    """Fetch M-Pesa access token"""
    token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(token_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    token_data = response.json()
    return token_data.get("access_token")

def lipa_na_mpesa(phone_number, amount):
    """Initiate STK Push"""
    access_token = get_mpesa_access_token()
    if not access_token:
        return {"error": "Failed to get access token"}

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode() 

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }

    response = requests.post(url, json=payload, headers=headers)  
    return response.json()

def process_mpesa_payment(data):
    transaction_id = data.get("TransID")
    amount = float(data.get("TransAmount", 0))
    phone_number = data.get("MSISDN")

    try:
        order = Order.objects.get(transaction_id=transaction_id, status="pending")
        if order.total_amount == amount:
            order.status = "Paid"
            order.save()
            return {"success": "Order payment confirmed"}
        else:
            return{"error": "Amount mismatch"}
    except Order.DoesNotExist:
        return {"error": "Order not found"}