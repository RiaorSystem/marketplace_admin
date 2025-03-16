from django.urls import path 
from .views import ChatListView, MessageListView, SendMessageView, SearchUserView, PostStatusView, GetStatusView

urlpatterns = [
    path("chats/", ChatListView.as_view(), name="chat_list"),
    path("chats/<int:chat_id>/messages/", MessageListView.as_view(), name="chat_messages"),
    path("chats/send/", SendMessageView.as_view(), name="send_message"),
    path("search/", SearchUserView.as_view(), name="send_message"),
    path("status/post/", PostStatusView.as_view(), name="post_status"),
    path("status/view/", GetStatusView.as_view(), name="view_status"),
] 