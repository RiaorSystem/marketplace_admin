from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Chat, Message, Status
from .serializers import ChatSerializer, MessageSerializer, StatusSerializer
from users.models import Contact, CustomUser
from users.serializers import ContactSerializer, UserSerializer
from django.db.models import Q
from rest_framework.generics import ListAPIView

class ChatListView(APIView):
    "List of people the user has chatted with or contacts"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = Chat.objects.filter(user1=request.user) | Chat.objects.filter(user2=request.user)
        contacts = Contact.objects.filter(owner = request.user, contact_user__isnull=False)
        chat_users = {chat.user1 for chat in chats} | {chat.user2 for chat in chats}
        contact_users = {contact.contact_user for contact in contacts}
        combined_users = list(chat_users | contact_users)
        serialized_users = ContactSerializer(combined_users, many=True).data

        return Response(serialized_users, status=status.HTTP_200_OK)


class MessageListView(APIView):
    """Chat history btn users """
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id, user1=request.user) or Chat.objects.get(id=chat_id, user2=request.user)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        
        messages = chat.messages.all()
        return Response(MessageSerializer(messages, many=True).data, status=status.HTTP_200_OK)
    
class SendMessageView(APIView):
    """Sending a new message & and updating chat history"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_username = request.data.get("receiver_username")
        content = request.data.get("content")

        if not receiver_username or not content:
            return Response({"error": "Receiver username and content are requikred"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver = CustomUser.objects.get(username=receiver_username)
        except CustomUser.DoesNotExist:
            return Response ({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user1, user2 =  sorted([sender, receiver], key=lambda x: x.id)
        chat, created = Chat.objects.get_or_create(user1=user1, user2=user2)
        message = Message.objects.create(chat=chat, sender=sender, content=content)

        chat.last_message = content
        chat.save()

        return Response(MessageSerializer(message). data, status=status.HTTP_201_CREATED)        
    

class SearchUserView(ListAPIView):
    """Search for users by name or username"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        return CustomUser.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) |Q(last_name__icontains=query)
        )


class PostStatusView(APIView):
    """Users can post status updtaes"""
    permission_classes = [ IsAuthenticated]

    def post(self, request):
        user = request.user
        text = request.data.get("text")
        image = request.FILES.get("image")

        if not text and not image :
            return Response({"error": "Status must have text or an image"}, status=status.HTTP_400_BAD_REQUEST)
        
        status_obj = Status.objects.create(user=user, text=text, image=image)
        return Response(StatusSerializer(status_obj).data, status=status.HTTP_201_CREATED)
    
class GetStatusView(APIView):
    """Users can see status updates of contacts"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts =  CustomUser.objects.filter(phone_number__in=[request.user.phone_number])
        statuses = Status.objects.filter(user__in=contacts)
        return Response(StatusSerializer(statuses, many=True).data, status=status.HTTP_200_OK)