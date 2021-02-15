from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

    def serialize_other(self):
        return {
            "username": self.username,
            "followers": len(self.followers.all()),
            "following": len(self.following.all()),
            "posts": [post.id for post in self.posts.all()],
            "follow_button": True 
        }

    def serialize_self(self):
        return {
            "username": self.username,
            "followers": str(len(self.followers.all())),
            "following": str(len(self.following.all())),
            "posts": [post.id for post in self.posts.all()]
        }


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"


class Posts(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    body = models.TextField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def serialize(self):
            return {
                "id": self.id,
                "user": self.user.username,
                "body": self.body,
                "created": self.created.strftime("%b %-d %Y, %-I:%M %p"),
                "likes": len(self.likers.all())
            }

    def __str__(self):
        return f"{self.user}: {self.body}"


class Likes(models.Model):
    post = models.ForeignKey(Posts, related_name="likers", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="liked_posts", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.post}"
