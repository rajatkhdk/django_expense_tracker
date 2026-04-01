from django.db import models
from django.utils import timezone

# from django.contrib.auth.models import User

# class Category(models.Model):
#     name = models.CharField(max_length=100)

#     icon = models.CharField(max_length=50, default='fas fa-circle')

#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name_plural = 'Categories'

# class Expense(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     date = models.DateField()
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.title} (${self.amount})"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    title =  models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places = 2)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"