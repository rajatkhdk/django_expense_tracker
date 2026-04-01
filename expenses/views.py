from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.db.models import Sum, Q
from .forms import ExpenseForm
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user # Attach the logged-in user
            expense.save()
            return redirect('dashboard') # Refresh page to show new data
    else:
        form = ExpenseForm()

    now = timezone.now()

    # Calculate the total of thiss month only
    current_month_total = Expense.objects.filter(
        user=request.user,
        date__year=now.year,
        date__month=now.month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Get the 5 most recent expenses
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]

    # Get the data for the Chart: Group by category name and sum the amounts
    category_data = Expense.objects.filter(user=request.user).values('category__name').annotate(total=Sum('amount')).order_by('-total')

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
    
@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
    return redirect('dashboard') # Safety redirect

@login_required
def edit_expense(request, pk):
    # Get the specific expense or retuen a 404 error
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

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

@login_required
def all_expenses(request):
    query = request.GET.get('search')

    # Start with only the current user's expenses
    user_expenses = Expense.objects.filter(user=request.user)

    if query:
      expenses = user_expenses.filter(
            Q(title__icontains=query) | 
            Q(category__name__icontains=query)
            ).order_by('-date')

    else:
        expenses = user_expenses.order_by('-date')

    return render(request, 'expenses/all_expenses.html', {'expenses': expenses, 'query': query})