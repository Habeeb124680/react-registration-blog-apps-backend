from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "text", "created_at", "like_count")
    list_filter = ("created_at",)
    search_fields = ("text", "author__email", "author__first_name")

    def like_count(self, obj):
        return obj.liked_by.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("text", "author__email", "author__first_name")