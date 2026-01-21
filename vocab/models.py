from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=200)
    example = models.TextField(blank=True)
    level = models.CharField(max_length=10, blank=True)
    topic = models.CharField(max_length=50, blank=True)


    def __str__(self):
        return self.word
