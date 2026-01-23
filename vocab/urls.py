from django.urls import path
from . import views

urlpatterns = [
    path("", views.today, name="today"),
    path("review/<int:word_id>/<str:result>/", views.review_word, name="review"),
]
