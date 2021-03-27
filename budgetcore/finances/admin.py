from django.contrib import admin
from .models import Bank, Expense, Category

# Register your models here.

admin.site.register(Bank)
admin.site.register(Expense)
admin.site.register(Category)