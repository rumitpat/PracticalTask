from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Content(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_submit = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Suggestion(models.Model):
    content = models.ForeignKey(Content, related_name="suggestions", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content.title} <-> {self.name}"


class SharePost(models.Model):
    content = models.ForeignKey(Content, related_name="share_post", on_delete=models.CASCADE)
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE)
