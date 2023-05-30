from rest_framework import serializers

class InfojobsAuthenticationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)
