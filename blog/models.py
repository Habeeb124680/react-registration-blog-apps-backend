from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    text = models.CharField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"