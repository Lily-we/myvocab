from django.urls import path
from .views import today

urlpatterns = [
    path('', today, name='today'),
]
