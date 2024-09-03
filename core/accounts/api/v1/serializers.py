from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Follow, Profile
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class UserSerializers(serializers.ModelSerializer):
#     #posts_author = PostSerializers(read_only= True, many= True)
#     #user_comment = CommentSerializers(read_only= True, many= True)
#     username = serializers.CharField(source='user.username', read_only=True)
#     email = serializers.CharField(source='user.email', read_only=True)
#     class Meta:
#         model = Profile
#         fields = ['id','username', 'email', 'active', 'descriptions']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
        read_only_fields = ["username"]


class ProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer(required=True, many=False)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "image",
            "active",
            "descriptions",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        username = self.data["user"]["username"]
        user = User.objects.get(username=username)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)
            return super(ProfileSerializers, self).update(
                instance, validated_data
            )
        else:
            raise ValidationError(
                {"error": "Bad request."}, code="invalid"
            )


class UserTestSerializers(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username", read_only=True
    )

    class Meta:
        model = Profile
        fields = ["id", "username"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    password1 = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "password does not match"}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"password": list(e.messages)}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class FollowersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "user", "follow_user"]
        read_only_fields = ["user"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserTestSerializers(instance.user).data
        rep["follow_user"] = UserTestSerializers(instance.follow_user).data
        return rep

    def create(self, validated_data):
        validated_data["user"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        relation = Follow.objects.filter(
            user=validated_data["user"],
            follow_user=validated_data["follow_user"],
        )
        if validated_data["follow_user"] == validated_data["user"]:
            raise ValidationError(
                {"error": "You cannot follow yourself."}, code="invalid"
            )
        elif relation.exists():
            raise ValidationError(
                {"error": "You cannot follow this user again."},
                code="invalid",
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["user"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        relation = Follow.objects.filter(
            user=validated_data["user"],
            follow_user=validated_data["follow_user"],
        )
        if validated_data["follow_user"] == validated_data["user"]:
            raise ValidationError(
                {"error": "You cannot follow yourself."}, code="invalid"
            )
        elif relation.exists():
            raise ValidationError(
                {"error": "You cannot follow this user again."},
                code="invalid",
            )
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=68, write_only=True)
    new_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    new_password1 = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"detail": "password does not match"}
            )
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(attrs)


class CustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(
                    msg, code="authorization"
                )
            if not user.profile.is_verified:
                raise serializers.ValidationError(
                    {"details": "user is not verified"}
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomAuthTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if not self.user.profile.is_verified:
            raise serializers.ValidationError(
                {"details": "user is not verified"}
            )
        validate_data["user_id"] = self.user.id
        validate_data["email"] = self.user.email
        return validate_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(
                    msg, code="authorization"
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        data["user"] = user
        return data


class ActivateResendSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100, required=True)

    def validate(self, attrs):
        username = attrs.get("user")
        try:
            user_profile = Profile.objects.get(user__username=username)
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            raise serializers.ValidationError(
                {"errors": "user does not exist"}
            )
        if user_profile.is_verified:
            raise serializers.ValidationError(
                {"errors": "user already verified"}
            )
        attrs["user"] = user
        return super().validate(attrs)


class ResetPasswordserializer(serializers.Serializer):
    user = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField()

    def validate(self, attrs):
        username = attrs.get("user")
        email = attrs.get("email")
        try:
            user_objects = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"errors": "user does not exist"}
            )
        if user_objects.email != email:
            raise serializers.ValidationError(
                {"errors": "username and email does not match"}
            )
        attrs["user"] = user_objects
        return super().validate(attrs)


class ResetPasswordConfirmserializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    new_password1 = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"detail": "password does not match"}
            )
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(attrs)
