from apps.hit_management.constants import (
    ERROR_MISSING_FIELDS,
    ERROR_INVALID_CREDENTIALS,
    ERROR_USER_DOES_NOT_EXIST,
)
from apps.hit_management.models import Hitman, Hit, Manager
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)
    first_name = serializers.CharField(max_length=128, required=False, allow_blank=True)

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.create_user(email=email, username=email, password=password)
        return user

    def validate_email(self, value):
        users = User.objects.filter(email=value)
        if len(users) > 0:
            raise serializers.ValidationError("This email is already registered.")

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "password")


class HitmanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    description = serializers.CharField(max_length=45, allow_blank=True, required=False)
    status = serializers.ChoiceField(
        choices=Hitman.HITMAN_STATUS, default="ACTIVE", required=False
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = data.pop("user", None)
        if user_data:
            data["user"] = user_data
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user_serializer = UserSerializer(data=validated_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.create(validated_data)

            hitman = Hitman.objects.create(user=user, **validated_data)
            return hitman

    def update_first_name(self, first_name, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.first_name = first_name
            user.save()
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError(ERROR_USER_DOES_NOT_EXIST)

    class Meta:
        model = Hitman
        fields = ("id", "user", "description", "status")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError(ERROR_INVALID_CREDENTIALS)
        else:
            raise serializers.ValidationError(ERROR_MISSING_FIELDS)

        attrs["user"] = user
        return attrs


class HitSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Hitman.objects.all()
    )
    creator = serializers.PrimaryKeyRelatedField(queryset=Hitman.objects.all())
    target_name = serializers.CharField(max_length=45)
    status = serializers.ChoiceField(
        choices=Hit.HIT_STATUS, default="OPENED", required=False
    )
    description = serializers.CharField(max_length=150)
    assignee_name = serializers.SerializerMethodField("get_assignee_name")
    creator_name = serializers.SerializerMethodField("get_creator_name")

    def get_assignee_name(self, obj):
        return obj.assignee.user.email if obj.assignee else ""

    def get_creator_name(self, obj):
        return obj.creator.user.email if obj.creator else ""

    class Meta:
        model = Hit
        fields = (
            "id",
            "creator",
            "assignee",
            "target_name",
            "status",
            "description",
            "assignee_name",
            "creator_name",
        )


class ManagerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=Hitman.objects.all(), required=False
    )
    lackeys = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Hitman.objects.all()
    )

    def update_is_staff(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.is_staff = 1
            user.save()
            return user
        except user.DoesNotExist:
            raise serializers.ValidationError(ERROR_USER_DOES_NOT_EXIST)

    class Meta:
        model = Manager
        fields = "__all__"
