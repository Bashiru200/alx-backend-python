from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerailizer, MessageSerializer

# Create your views here.
class ConversationViewSets(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('message', 'participant')
    serializer_class = ConversationSerailizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__user_id']



    def create(self, request, *args, **kwargs):
        # create a conversation with participant
        participants_id = request.data.get('participants')
        if not participants_id or not isinstance(participants_id, list):
            return Response({"error: participant must be a list of user IDs"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        conversation = conversation.objects.create()
        conversation.participants.set(participants_id)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSets(viewsets.ModelViewSet):
    # queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['participants__user_id']

#     def  create(self, request, *args, **kwargs):
#         #send message to an existing conversation
#         conversation_id = request.data.get('conversation')
#         sender_id = request.data.get('sender')
#         body = request.data.get('message_body')

#         if not (conversation_id and sender_id and body):
#             return Response({"error": "Missing required fields."},
#                             status=status.HTTP_400_BAD_REQUEST)
        

#         try:
#             conversation = Conversation.objects.get(pk=conversation_id)
#         except Conversation.DoesNotExist:
#             return Response({"error": "Conversation not found."},
#                             status=status.HTTP_404_NOT_FOUND)

#         message = Message.objects.create(
#             sender_id=sender_id,
#             conversation=conversation,
#             message_body=body
#         )
#         serializer = self.get_serializer(message)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# #NEWLINE

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        serializer.save(conversation_id=conversation_id)
