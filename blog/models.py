from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    text = models.CharField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # true once the text has been changed after posting
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]  # oldest first, like a conversation

    def __str__(self):
        return f"{self.author} on post {self.post_id}: {self.text[:30]}"