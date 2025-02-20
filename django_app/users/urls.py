from django.urls import path 
from .views import SignUpView
from .views import SignInView
from .views import ProfileView
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('profile/',ProfileView.as_view(),name = 'profile')
]