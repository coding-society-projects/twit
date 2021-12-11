from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')




class Posting(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    posted_on = models.DateTimeField(default=datetime.now, blank=True)
    likes = models.ManyToManyField(User, related_name='posting_like')

    def __str__(self):
        return self.content

    def total_likes(self):
        return self.likes.count()

