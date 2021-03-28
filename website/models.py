"""Models"""
from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Film(models.Model):
    id_title = models.CharField(max_length=100000)
    name = models.CharField(max_length=10000, default="-")
    year = models.CharField(max_length=10000, default="0")
    genre = models.CharField(max_length=10000, default="-")
    country = models.CharField(max_length=10000, default="USA")
    budget = models.CharField(max_length=10000000, default=0)
    duration = models.IntegerField(default=10)
    rating = models.DecimalField(max_digits=5, decimal_places=3, default=0)

    def __str__(self):
        return f"{self.name} {self.id_title}"


class Film_with_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id} {self.film.id_title}"
