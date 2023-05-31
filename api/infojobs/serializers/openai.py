from rest_framework import serializers

class AnalizeSerializer(serializers.Serializer):
    texto = serializers.CharField(required=True)