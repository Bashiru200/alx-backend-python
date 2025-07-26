from rest_framework import serializers
from rest_framework.serializers import CharField, ValidationError

from .models import Users, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
from rest_framework import serializers
from rest_framework.serializers import CharField, ValidationError
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    first_name = CharField(max_length=100)

    class Meta:
        model = Users
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]
    def validate_first_name(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError("First and Last name cannot use number.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
        ]

class ConversationSerailizer(serializers.ModelField):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
        ]