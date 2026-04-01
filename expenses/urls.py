from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('all/', views.all_expenses, name='all_expenses'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('edit/<int:pk>', views.edit_expense, name='edit_expense'),
]