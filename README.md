# 🛒 Betanet Marketplace Backend

A full-stack eCommerce marketplace built with **Django REST Framework (DRF)** & **FastAPI** for:
- 🕒 **Real-time order tracking** (via WebSockets)
- 💰 **M-Pesa & Stripe payments**
- 🔐 **Escrow System for secure transactions**

## 🚀 Features Implemented So Far

### 1️⃣ User Authentication
✅ Custom User Model (Email-based Login)  
✅ User Registration & Login (JWT Authentication)  
✅ OAuth Login (Google, Facebook, Twitter)  

### 2️⃣ User Profile & Roles
✅ Buyers & Sellers Roles  
✅ Profile Picture Upload (Post-Signup)  

### 3️⃣ Seller Dashboard
✅ Sellers Can List Products  
✅ Sales Analytics  

### 4️⃣ Product Listings & Search
✅ Product Categories  
✅ Search by Name, Category, Price, Rating  
✅ Product Image Uploads (Cloudinary/S3)  
✅ CRUD Operations for Sellers  

### 5️⃣ Shopping Cart & Checkout
✅ Add/Remove Items in Cart  
✅ Order Creation from Cart  

### 6️⃣ Payment Integration
✅ **M-Pesa** (Daraja API)  
✅ **Visa/MasterCard** (Stripe)  
✅ Automatic Order Confirmation After Payment  

### 7️⃣ Real-Time Order Tracking (FastAPI)
✅ WebSockets for Instant Order Updates  
✅ Buyers Get Real-Time Order Status from Sellers  

### 8️⃣ Escrow System for Advertisements
✅ **Secure Transactions Between Sellers & Advertisers**  
✅ **Funds Are Held in Escrow Until Ad Completion**  
✅ **Buyers (Advertisers) Apply for Advertisement Opportunities**  
✅ **Engagement Stats Are Submitted via Image Upload or Social Media Link**  
✅ **Sellers Approve Applications & Release Funds to Advertisers**  


### 🔜 Next Steps
🚧 **Admin Dashboard** (Manage Orders & Payments)  

---

## 📌 Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/betanet-marketplace.git
cd betanet-marketplace
```

### 2️⃣ Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.\.venv\Scriptsctivate   # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the root directory and add:

```ini
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# M-Pesa API Keys
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=http://127.0.0.1:8000/api/payments/mpesa/webhook/

# Stripe API Keys
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

### 5️⃣ Run Database Migrations
```bash
python manage.py makemigrations users products orders payments
python manage.py migrate
```

### 6️⃣ Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7️⃣ Start Django Backend
```bash
python manage.py runserver
```
📍 Open API Docs: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

### 8️⃣ Start FastAPI for Real-Time Order Tracking
```bash
uvicorn fastapi_app.tracking:app --host 0.0.0.0 --port 8001 --reload
```
📍 Open FastAPI Docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## 📌 API Testing

### 1️⃣ User Authentication
#### ✅ Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "johndoe@example.com", "password": "securepassword"}'
```

#### ✅ Login & Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "johndoe@example.com", "password": "securepassword"}'
```
📌 **Response Example:**
```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```

---

### 2️⃣ Product Management
#### ✅ Create a Product (Seller Only)
```bash
curl -X POST http://127.0.0.1:8000/api/products/create/ -H "Authorization: Bearer your_jwt_access_token" -H "Content-Type: application/json" -d '{"name": "Smartphone", "description": "Latest model", "price": 500, "category_id": 1}'
```

#### ✅ Search Products
```bash
curl -X GET "http://127.0.0.1:8000/api/products/?category=electronics&min_price=100"
```

---

### 3️⃣ M-Pesa Payment
#### ✅ Initiate Payment
```bash
curl -X POST http://127.0.0.1:8000/api/payments/mpesa/ -H "Authorization: Bearer your_jwt_access_token" -H "Content-Type: application/json" -d '{"phone_number": "254712345678", "amount": 100}'
```

---

### 4️⃣ Real-Time Order Tracking
#### ✅ Connect WebSocket to Track Order
```bash
websocat ws://127.0.0.1:8001/track_order/1
```

#### ✅ Seller Updates Order Status
```bash
curl -X PUT http://127.0.0.1:8000/api/orders/1/update/ -H "Authorization: Bearer seller_jwt_access_token" -H "Content-Type: application/json" -d '{"status": "processing"}'
```
📌 **WebSocket Response Example:**
```json
{"order_id": 1, "status": "processing"}
```


### 5️⃣ API Testing for Escrow System

### ✅ Create an Advertisement (Seller Only)
```bash
curl -X POST http://127.0.0.1:8000/api/escrow/ads/create/ -H "Authorization: Bearer seller_jwt_access_token" -H "Content-Type: application/json" -d '{                    
    "title": "Promote my product",
    "description": "Advertise my new brand",
    "budget": 50,
    "duration": 7
}'
```
 **Expected Response**
```json
{"id": 1, "title": "Promote my product", "budget": 50, "duration": 7}
```

---

### ✅ Apply for Advertisement (Buyer)
```bash
curl -X POST http://127.0.0.1:8000/api/escrow/ads/1/apply/ -H "Authorization: Bearer buyer_jwt_access_token" -H "Content-Type: application/json" -d '{}'
```
 **Expected Response**
```json
{"id": 1, "advertiser_name": "buyer1", "advertisement_title": "Promote my product"}
```

---

### ✅ Submit Engagement Stats (Image Upload or Social Media Link)
 **Submit Engagement Proof via Image Upload**
```bash
curl -X POST http://127.0.0.1:8000/api/escrow/ads/1/submit-stats/ -H "Authorization: Bearer buyer_jwt_access_token" -F "engagement_photo=@/path/to/photo.jpg"
```
 **OR Submit a Social Media Link**
```bash
curl -X POST http://127.0.0.1:8000/api/escrow/ads/1/submit-stats/ -H "Authorization: Bearer buyer_jwt_access_token" -H "Content-Type: application/json" -d '{"engagement_link": "https://tiktok.com/post/1234"}'
```
 **Expected Response**
```json
{"message": "Engagement stats submitted"}
```

---

### ✅ Approve Advertisement & Release Funds (Seller)
```bash
curl -X POST http://127.0.0.1:8000/api/escrow/ads/1/approve/ -H "Authorization: Bearer seller_jwt_access_token"
```
 **Expected Response**
```json
{"message": "Funds released to advertiser"}
```


