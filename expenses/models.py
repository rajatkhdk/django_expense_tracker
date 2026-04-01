from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __clstr__(self):
        return self.name
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title =  models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places = 2)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"