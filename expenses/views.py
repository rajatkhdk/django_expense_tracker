from django.shortcuts import render, redirect
from .models import Expense
from django.db.models import Sum
from .forms import ExpenseForm
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404

# Create your views here.
def dashboard(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # Refresh page to show new data
    else:
        form = ExpenseForm()

    now = timezone.now()

    # Calculate the total of thiss month only
    current_month_total = Expense.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Get the 5 most recent expenses
    recent_expenses = Expense.objects.all().order_by('-date')[:5]

    # Get the data for the Chart: Group by category name and sum the amounts
    category_data = Expense.objects.values('category__name').annotate(total=Sum('amount')).order_by('-total')

    # Extract labels and values for JavaScript
    labels = [item['category__name'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    context = {
        'total_expenses': current_month_total, # this is now filtered
        'recent_expenses': recent_expenses,
        'form' : form,  # Send the form to the HTML
        'current_month_name': now.strftime('%B'), # Sends "April" to the UI
        'labels': labels,   # List of names like ['Food', 'Rent']
        'data': data,   # List of numbers like [50.00, 1200.00]
    }

    return render(request, 'expenses/dashboard.html', context)

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return redirect('dashboard') # Safety redirect

def edit_expense(request, pk):
    # Get the specific expense or retuen a 404 error
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        # Fill the form with the new data from the user, but linked to the old instance
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Get request: Show the form pre-filled with existing data
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/edit_expense.html', {
        'form': form,
        'expense': expense
    })

def all_expenses(request):
    query = request.GET.get('search')
    if query:
      expenses = Expense.objects.filter(title__icontains=query).order_by('-date')

    else:
        expenses = Expense.objects.all().order_by('-date')

    return render(request, 'expenses/all_expenses.html', {'expenses': expenses, 'query': query})