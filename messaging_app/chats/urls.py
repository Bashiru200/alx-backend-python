from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSets, MessageViewSets

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSets, basename='conversation')

#Nested router for messages
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='converstaions')
conversation_router.register(r'messages', MessageViewSets, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls))
]
