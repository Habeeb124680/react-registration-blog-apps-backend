from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    PostListCreateView,
    LikeToggleView,
    PostDetailView,
    PostCommentsView,
    CommentDetailView,
)

urlpatterns = [
    path("auth/register", RegisterView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/me", MeView.as_view()),
    path("posts", PostListCreateView.as_view()),
    path("posts/<int:post_id>/like", LikeToggleView.as_view()),
    path("posts/<int:post_id>", PostDetailView.as_view()),
    path("posts/<int:post_id>/comments", PostCommentsView.as_view()),
    path("comments/<int:comment_id>", CommentDetailView.as_view()),
]