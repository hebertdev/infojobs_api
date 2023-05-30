from rest_framework import serializers

# models
from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'infojobs_id',
            'username',
            'first_name',
            'last_name',
        )





