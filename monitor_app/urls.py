from django.urls import path
from .views import *


urlpatterns = [
    path('', homeView, name='home_url'),
    path('sign_in', signInView, name='sign_in_url'),
    path('sign_out', signOutView, name='sign_out_url'),
    path('sign_up', signUpView, name='sign_up_url'),
    path('profile', profileView, name='profile_url'),
    path('change_profile', changeProfileView, name='change_profile_url'),
    path('add_funds', addFundsView, name='add_funds_url'),
    path('categories', categoriesView, name='categories_url'),
    path('expenses_by_category/<int:category_id>', expensesByCategoryView, name='expenses_by_category_url'),
    path('add_expense', addExpenseView, name='add_expense_url'),
    path('reset_button', resetWalletView, name='reset_wallet_url'),
]
