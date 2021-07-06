from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime


class User(AbstractUser):
    followings = models.ManyToManyField('User', related_name='_followings')
    followers = models.ManyToManyField('User', related_name='_followers')
    liked = models.ManyToManyField('Post')


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    like = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Post {self.id} by {self.poster}'
