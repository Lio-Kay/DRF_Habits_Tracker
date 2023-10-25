from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'id', 'email', 'tg_name',
        read_only_fields = 'chat_id', 'update_id',
