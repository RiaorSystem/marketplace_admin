import requests, base64
from django.conf import settings 
from .models import EscrowWallet

MPESA_AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
MPESA_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret =  settings.MPESA_CONSUMER_SECRET
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encoded()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(MPESA_AUTH_URL, headers=headers)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        raise Exception("Failed to get M-Pesa access token")

def lipa_na_mpesa(seller, phone_number, amount):
    access_token = get_mpesa_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content_Type":"application/json"}

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "Escrow Deposit",
        "TransactionDesc": "Deposit to Escrow Wallet"
    }

    response = requests.post(MPESA_URL, json=payload, headers=headers)

    if response.status_code == 200:
        wallet, created = EscrowWallet.objects.get_or_create(owner=seller)
        wallet.deposit(amount)
        return {"message": "Deposit successful", "wallet_balance":wallet.balance}
    return {"error": "M-Pesa payment failed"}