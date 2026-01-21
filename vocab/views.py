from django.shortcuts import render
from .models import Word

def today(request):
    words = Word.objects.all().order_by("-id")[:10]
    return render(request, "vocab/today.html", {"words": words})
