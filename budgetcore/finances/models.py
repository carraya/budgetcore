from django.db import models
from django.utils.text import slugify

# Create your models here.

class Bank(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    balance = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Bank, self).save(*args, **kwargs)
        
    def balance_left(self):
        expense_list = Expense.objects.filter(bank=self)
        total_expense_amount = 0
        for expense in expense_list:
            if expense.category.name != 'Bill' and expense.category.name != 'bill':
                total_expense_amount += expense.amount
        
        return self.balance - total_expense_amount

    def bills(self):
        expense_list = Expense.objects.filter(bank=self)
        bill_expense_amount = 0
        for expense in expense_list:
            if expense.category.name == 'Bill' or expense.category.name == 'bill':
                bill_expense_amount += expense.amount

        return bill_expense_amount

    def surplus(self):
        bill_expense_amount = self.bills()
        return self.balance_left() - bill_expense_amount 

class Category(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Expense(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-amount',)