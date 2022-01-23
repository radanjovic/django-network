from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField("New Post")
    created = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} : {self.content[:10]}..."


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} likes {self.post}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} follows {self.following}"