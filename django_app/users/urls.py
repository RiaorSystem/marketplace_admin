from django.urls import path, include
from .views import SignInView, SignUpView,ProfileView, ChangePasswordView, SyncContactsView, GetContactsView
from .views import SignInView, SignUpView,ProfileView, ChangePasswordView, AdminUserListView, AdminUserDetailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), 
    path('google/', include('allauth.socialaccount.urls')), 
    path('contacts/sync/', SyncContactsView.as_view(), name='sync_contacts'),
    path('contacts/', GetContactsView.as_view(), name="get_contacts"),
    path("admin/users/", AdminUserListView.as_view(), name="admin_users"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
]