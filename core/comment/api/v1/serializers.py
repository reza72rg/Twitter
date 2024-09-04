from django.db.models import Q
from rest_framework import serializers
from comment.models import Comment
from accounts.api.v1.serializers import UserTestSerializers
from rest_framework.exceptions import ValidationError
from accounts.models import Follow
from blog.models import Post


class CommentSerializers(serializers.ModelSerializer):
    snippet = serializers.CharField(source="get_snippet", read_only=True)
    relative_url = serializers.URLField(
        source="get_absolute_url", read_only=True
    )
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "content",
            "snippet",
            "relative_url",
            "absolute_url",
            "author",
        ]
        read_only_fields = ["author"]

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
            instance.author,
        ).data
        return rep

    def create(self, validated_data):
        user = self.context["request"].user.profile
        validated_data["author"] = user
        validated_data["approach"] = False

        if not Post.objects.filter(
            (
                Q(
                    author__in=Follow.objects.filter(
                        user=user
                    ).values_list("follow_user", flat=True)
                )
                | Q(author=user)
            )
            & Q(id=validated_data["post"].id)
            & Q(archive=True)
        ).exists():
            raise ValidationError(
                {
                    "error": "You do not have permission to comments on this post."
                },
                code="invalid",
            )
        return super().create(validated_data)

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)
