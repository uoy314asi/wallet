from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
import requests


def homeView(request):
    return render(request, 'home.html')


def signInView(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('home_url')
        else:
            return redirect('sign_in_url')


def signOutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home_url')


def signUpView(request):
    if request.method == 'GET':
        return render(request, 'sign_up.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        if AccountHolder.objects.filter(email=email):
            return render(request, 'sign_up.html', {'msg': 'Email is not valid'})
        else:
            user = AccountHolder(email=email)
            user.set_password(password)
            user.save()
            return redirect('sign_in_url')


def profileView(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'wallet': round(request.user.wallet, 2)})
    else:
        return redirect('sign_in_url')


def changeProfileView(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'change_profile.html')
        elif request.method == 'POST':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            if request.user.name != name:
                request.user.name = name
            if request.user.surname != surname:
                request.user.surname = surname
            request.user.save()
            return redirect('profile_url')
    else:
        return redirect('sign_in_url')


def addFundsView(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            currencies = [elem[0] for elem in CURRENCY_CHOICES]
            return render(request, 'add_funds.html', {'currencies': currencies})
        elif request.method == 'POST':
            funds = int(request.POST.get('funds'))
            currency = request.POST.get('currency')
            if request.user.currency == currency:
                request.user.wallet += funds
            else:
                url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/'
                url += str(currency).lower() + '.json'
                response = requests.get(url)
                data = response.json()[str(currency).lower()]
                request.user.wallet += funds * data[str(request.user.currency).lower()]
            request.user.save()
            return redirect('profile_url')
    else:
        return redirect('sign_in_url')


def categoriesView(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {
                'categories': []
            }
            categories = request.user.categories.all()
            for category in categories:
                expenses = request.user.expenses.filter(category=category)
                category_sum = 0
                for expense in expenses:
                    category_sum += expense.amount
                context['categories'].append({
                    'id': category.id,
                    'name': category.name,
                    'amount': round(category_sum, 2)
                })
            return render(request, 'categories.html', context)
        elif request.method == 'POST':
            category_name = request.POST.get('category_name')
            if request.user.categories.filter(name=category_name):
                return redirect('categories_url')
            category = Category(name=category_name)
            category.save()
            request.user.categories.add(category)
            request.user.save()
            return redirect('categories_url')
    else:
        return redirect('sign_in_url')


def expensesByCategoryView(request, category_id):
    if request.user.is_authenticated:
        category = request.user.categories.get(id=category_id)
        expenses = request.user.expenses.filter(category=category)
        for expense in expenses:
            expense.amount = round(expense.amount, 2)
        context = {
            'expenses': expenses,
            'category': category
        }
        return render(request, 'expenses_by_category.html', context)
    else:
        return redirect('sign_in_url')


def addExpenseView(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {
                'currencies': [elem[0] for elem in CURRENCY_CHOICES],
                'categories': request.user.categories
            }
            return render(request, 'add_expense.html', context)
        elif request.method == 'POST':
            name = request.POST.get('name')
            amount = int(request.POST.get('amount'))
            currency = request.POST.get('currency')
            category = request.user.categories.get(id=request.POST.get('category'))
            created_at = request.POST.get('created_at')
            if currency == request.user.currency:
                amount = amount * 1
            else:
                url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/'
                url += str(currency).lower() + '.json'
                response = requests.get(url)
                data = response.json()[str(currency).lower()]
                amount *= data[str(request.user.currency).lower()]
            expense = Expense(name=name, amount=amount, category=category, created_at=created_at)
            expense.save()
            request.user.expenses.add(expense)
            request.user.wallet -= amount
            request.user.save()
            return redirect('add_expense_url')
    else:
        return redirect('sign_in_url')


def resetWalletView(request):
    if request.user.is_authenticated:
        request.user.wallet = 0
        request.user.save()
        return redirect('profile_url')
    else:
        return redirect('sign_in_url')
