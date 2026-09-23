from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    # Django's built-in User has first_name/last_name, not "name" —
    # we store the display name in first_name and expose it as "name".
    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ["id", "name", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, max_length=50)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],  # we log in with email, Django needs a username internally
            email=validated_data["email"],
            first_name=validated_data["name"],
            password=validated_data["password"],  # create_user hashes this automatically
        )
        return user


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()
    is_own = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "text", "created_at", "author", "like_count", "liked_by_me", "is_own"]

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def get_liked_by_me(self, obj):
        user = self.context["request"].user
        return user.is_authenticated and obj.liked_by.filter(id=user.id).exists()

    def get_is_own(self, obj):
        user = self.context["request"].user
        return user.is_authenticated and obj.author_id == user.id


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text"]