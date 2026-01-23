from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Word

def today(request):
    # show words due for review
    words = Word.objects.filter(next_review__lte=timezone.now()).order_by("next_review")[:20]
    return render(request, "vocab/today.html", {"words": words})

def review_word(request, word_id, result):
    if request.method != "POST":
        return redirect("today")

    word = get_object_or_404(Word, id=word_id)

    word.times_seen += 1
    word.last_reviewed = timezone.now()

    if result == "forgot":
        word.times_failed += 1
        word.next_review = timezone.now() + timedelta(days=1)
    else:
        word.next_review = timezone.now() + timedelta(days=3)

    word.save()
    return redirect("today")
