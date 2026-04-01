from django.contrib import admin
from .models import Category, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date', 'user')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'description')
