Betanet Marketplace - Backend 🚀
A multi-vendor marketplace backend built with Django & FastAPI, supporting user authentication, role management, social login, and profile updates.

🔹 Features Implemented
✅ User Authentication (Signup, Login, JWT)
✅ User Roles (Admin, Seller, Buyer)
✅ Profile Management (Update Info, Change Password, Upload Profile Picture)
✅ Social Login (Google, Facebook, Twitter, Instagram)

🔹 API Endpoints
📍 Authentication

POST /api/auth/register/ – User Signup
POST /api/auth/login/ – User Login
POST /api/auth/logout/ – Logout
📍 Profile Management

GET /api/auth/profile/ – View Profile
PUT /api/auth/profile/ – Update Profile
PUT /api/auth/profile-picture/ – Upload Profile Picture
POST /api/auth/change-password/ – Change Password
📍 Social Authentication

GET /api/auth/google/login/ – Google Login
GET /api/auth/facebook/login/ – Facebook Login
🔹 How to Run Locally
1️⃣ Install Dependencies


pip install -r requirements.txt
2️⃣ Run Migrations


python manage.py makemigrations
python manage.py migrate
3️⃣ Start the Server


python manage.py runserver
