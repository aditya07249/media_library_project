from rest_framework import serializers
from .models import MediaFile, Category
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'
        read_only_fields = ['owner','size']

    def create(self, validated_data):
        uploaded_file = validated_data.get("file")
        if uploaded_file:
            validated_data["size"] = uploaded_file.size
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

