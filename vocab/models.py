from django.db import models
from django.utils import timezone

class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)
    translation = models.CharField(max_length=255)
    example = models.TextField(blank=True)

    # 🧠 learning state
    times_seen = models.PositiveIntegerField(default=0)
    times_failed = models.PositiveIntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.word
