from .models import UsersData
from rest_framework import serializers

#serializer for user data Model
class UsersDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersData
        fields = '__all__'
