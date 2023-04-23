from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
