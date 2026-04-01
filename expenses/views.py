from django.shortcuts import render, redirect
from .models import Expense
from django.db.models import Sum
from .forms import ExpenseForm

# Create your views here.
def dashboard(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # Refresh page to show new data
    else:
        form = ExpenseForm()

    # Calculate the total of all expenses in the database
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # Get the 5 most recent expenses to show in a table
    recent_expenses = Expense.objects.all().order_by('-date')[:5]

    context = {
        'total_expenses': total_expenses,
        'recent_expenses': recent_expenses,
        'form' : form,  # Send the form to the HTML
    }

    return render(request, 'expenses/dashboard.html', context)