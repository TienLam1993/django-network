from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followings = models.ManyToManyField('User', related_name='_followings')
    followers = models.ManyToManyField('User', related_name='_followers')
    liked = models.ManyToManyField('Post')


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Post {self.id} by {self.poster}'

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "date_created": self.date.strftime("%m/%d/%Y, %H:%M:%S"),
            "last_modified": self.last_modified.strftime("%m/%d/%Y, %H:%M:%S"),
            "like": self.like
        }
