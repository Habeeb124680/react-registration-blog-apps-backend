from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Post, Comment
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)


def token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "access_token": token_for_user(user),
                "token_type": "bearer",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Incorrect email or password"}, status=401)

        # Django logs in by "username" internally — we set username = email at registration.
        user = authenticate(username=user_obj.username, password=password)
        if user is None:
            return Response({"detail": "Incorrect email or password"}, status=401)

        return Response(
            {
                "access_token": token_for_user(user),
                "token_type": "bearer",
                "user": UserSerializer(user).data,
            }
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        return PostCreateSerializer if self.request.method == "POST" else PostSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(PostSerializer(post, context={"request": request}).data, status=201)


class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)

        return Response(PostSerializer(post, context={"request": request}).data)


class PostDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        if post.author_id != request.user.id:
            return Response({"detail": "You can only delete your own posts"}, status=403)

        post.delete()
        return Response(status=204)


class PostCommentsView(APIView):
    """GET: anyone can read a post's comments. POST: logged-in users can add one."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        comments = post.comments.select_related("author")
        return Response(CommentSerializer(comments, many=True, context={"request": request}).data)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(post=post, author=request.user)
        return Response(
            CommentSerializer(comment, context={"request": request}).data, status=201
        )


class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=404)

        if comment.author_id != request.user.id:
            return Response({"detail": "You can only delete your own comments"}, status=403)

        comment.delete()
        return Response(status=204)