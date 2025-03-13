from django.urls import path 
from .views import SignUpView
from .views import SignInView
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
]