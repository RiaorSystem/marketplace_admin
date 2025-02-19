from django.urls import path, include
from .views import SignInView, SignUpView,ProfileView, ChangePasswordView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), 
    path('google/', include('allauth.socialaccount.urls')), 
]