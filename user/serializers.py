
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics
from .models import *
from djoser.conf import settings

from django.contrib.auth.tokens import default_token_generator

# from .services import send_email




import logging
logger = logging.getLogger(__name__)

class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = '__all__'

class UserNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNetwork
        fields = '__all__'

class UserSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            'fio',
            "phone",
            "uuid",
        ]

class UserSerializer(serializers.ModelSerializer):
    networks = UserNetworkSerializer(many=True, required=False, read_only=True)
    files = UserFileSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
                "uuid",
                "login",
                "fio",
                "phone",
                "is_private",
                "is_vip",
                "is_problem",
                "is_manager",
                "is_staff",
                'date_joined',
            'email',
            'comment',
            'files',
            'networks'

        ]

        extra_kwargs = {
            'password': {'required': False},

        }


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'added_by',
            'fio',
            'phone',
            'login',
            'password',
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")


        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            print(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = True
            user.save(update_fields=["is_active"])

        return user


