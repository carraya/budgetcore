from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.banks_list, name='bank_list'),
    path('add', views.BankCreateView.as_view(), name='add'),
    path('<slug:bank_slug>', views.finance_info, name='finance_info'),
]