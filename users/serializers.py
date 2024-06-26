from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from rest_framework.exceptions import ValidationError
from ipdb import set_trace

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )
        ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    class Meta:
        model = User
        fields = [
            "id", "username", "email",  "full_name", "artistic_name", "password",
            "full_name", "artistic_name"
            ]
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
