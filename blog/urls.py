from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    PostListCreateView,
    LikeToggleView,
    PostDeleteView,
    PostCommentsView,
    CommentDeleteView,
)

urlpatterns = [
    path("auth/register", RegisterView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/me", MeView.as_view()),
    path("posts", PostListCreateView.as_view()),
    path("posts/<int:post_id>/like", LikeToggleView.as_view()),
    path("posts/<int:post_id>", PostDeleteView.as_view()),
    path("posts/<int:post_id>/comments", PostCommentsView.as_view()),
    path("comments/<int:comment_id>", CommentDeleteView.as_view()),
]