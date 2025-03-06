from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False ,related_name = "followers", null=True, blank=True)
    
    def __str__(self):
        return self.username

class Thread(models.Model):
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name="threads")
    body = models.CharField(max_length = 500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes_by_user")
    like_count = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "creator": {
                "id": self.creator.id,
                "username": self.creator.username
            },
            "body": self.body,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": [
                {"id": user.id, "username": user.username}
                for user in self.likes.all()
            ],
            "like_count": self.like_count,
        }