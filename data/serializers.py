
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import exceptions, serializers, status, generics
from .models import *
from user.serializers import UserSaveSerializer

from django.contrib.auth.tokens import default_token_generator


import logging
logger = logging.getLogger(__name__)


class PayStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayStatus
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'
class ServiceTabSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTab
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    tabs = ServiceTabSerializer(many=True, required=False, read_only=True)
    countries = CountrySerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Service
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'




class DirectionSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Direction
        fields = '__all__'




class OrderFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFile
        fields = '__all__'

class OrderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderComment
        fields = '__all__'


class OrderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    files = OrderFileSerializer(many=True, required=False, read_only=True)
    comments = OrderCommentSerializer(many=True, required=False, read_only=True)
    user = UserSaveSerializer(many=False, required=True, read_only=False)
    pay_status = PayStatusSerializer(many=False, required=True, read_only=False)
    order_status = OrderStatusSerializer(many=False, required=True, read_only=False)
    category = CategorySerializer(many=False, required=True, read_only=False)
    service = ServiceSerializer(many=False, required=True, read_only=False)
    # created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_by = UserSaveSerializer(many=False, required=True, read_only=False)
    class Meta:
        model = Order
        fields = '__all__'

    # def create(self, validated_data):
    #     print(validated_data)
    #     category_data = validated_data.pop('category')
    #
    #     # order = Order.objects.create(**validated_data)
    #     return














