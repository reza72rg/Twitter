from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ...models import Like, DisLike, Category, Post
from accounts.api.v1.serializers import UserTestSerializers
from accounts.models import Follow, Profile


class PostSerializersArchive(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    snippet = serializers.CharField(source="get_snippet", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "snippet",
            "absolute_url",
            "archive",
            "author",
        ]
        read_only_fields = ["author", "content"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("absolute_url")
            rep.pop("snippet")
        else:
            rep.pop("content")
        rep["author"] = UserTestSerializers(
            instance.author, context={"request": request}
        ).data
        return rep


class PostSerializers(serializers.ModelSerializer):
    snippet = serializers.CharField(source="get_snippet", read_only=True)
    relative_url = serializers.URLField(
        source="get_absolute_url", read_only=True
    )
    absolute_url = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "image",
            "category",
            "snippet",
            "relative_url",
            "absolute_url",
            "archive",
            "author",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet")
            rep.pop("absolute_url")
            rep.pop("relative_url")
        else:
            rep.pop("content")
        rep["author"] = UserTestSerializers(
            instance.author, context={"request": request}
        ).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user"]
        read_only_fields = ["user"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserTestSerializers(instance.user).data
        return rep

    def create(self, validated_data):
        user = self.context["request"].user.profile
        validated_data["user"] = user

        # Ensure the user is liking a post they have permission to like
        if not Post.objects.filter(
            (Q(author__in=Follow.objects.filter(user=user).values_list(
                "follow_user", flat=True)) | Q(author=user)) & Q(id=validated_data["post"].id) & Q(
                archive=True)).exists():
            raise ValidationError({"error": "You do not have permission to like this post."}, code="invalid", )

        relation = Like.objects.filter(
            user=validated_data["user"], post=validated_data["post"]
        )

        if relation.exists():
            raise ValidationError(
                {"error": "You cannot Like this post again."},
                code="invalid",
            )
        return super().create(validated_data)


class DislikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ["id", "post", "user"]
        read_only_fields = ["user"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserTestSerializers(instance.user).data
        return rep

    def create(self, validated_data):
        user = self.context["request"].user.profile
        validated_data["user"] = user
        if not Post.objects.filter(
            (Q(author__in=Follow.objects.filter(user=user).values_list("follow_user", flat=True)) | Q(author=user)) & Q(
                id=validated_data["post"].id) & Q(archive=True)).exists():
            raise ValidationError(
                {"error": "You do not have permission to Dislike this post."}, code="invalid",)

        relation = DisLike.objects.filter(user=user, post=validated_data["post"])
        if relation.exists():
            raise ValidationError(
                {"error": "You cannot DisLike this post again."}, code="invalid",)
        return super().create(validated_data)


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
